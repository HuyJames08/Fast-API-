from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(User):
    """Response without sensitive fields"""
    pass