from datetime import timedelta
from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.core.security import create_access_token
from app.core.config import settings


class AuthService:
    """Business logic for authentication"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    def register(self, email: str, password: str):
        """Register new user"""
        # Check if user already exists
        existing_user = self.user_service.get_user_by_email(email)
        if existing_user:
            return None, "Email already registered"
        
        # Create new user
        user_create = UserCreate(email=email, password=password)
        user = self.user_service.create_user(user_create)
        return user, None
    
    def login(self, email: str, password: str):
        """Login user and return JWT token"""
        user = self.user_service.authenticate_user(email, password)
        if not user:
            return None, "Invalid email or password"
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "user": {"id": user.id, "email": user.email}}, None