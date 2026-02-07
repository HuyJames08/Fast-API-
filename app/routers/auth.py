from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse, MeResponse, Token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to provide UserService"""
    return UserService(db)


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    """Dependency to provide AuthService"""
    return AuthService(user_service)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Register a new user"""
    user, error = auth_service.register(request.email, request.password)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Generate access token for the newly registered user
    from app.core.security import create_access_token
    from datetime import timedelta
    from app.core.config import settings
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
    }


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login user and get access token"""
    result, error = auth_service.login(request.email, request.password)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return result


@router.get("/me", response_model=MeResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }