from sqlalchemy import Column, String, Boolean
from app.models.base import Base, BaseModel


class User(BaseModel):
    """User ORM Model"""
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)