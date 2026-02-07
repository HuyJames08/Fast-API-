from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict  # User info


class MeResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True