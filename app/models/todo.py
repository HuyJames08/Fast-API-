from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModel


class Todo(BaseModel):
    """Todo ORM Model"""
    __tablename__ = "todos"
    
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationship
    owner = relationship("User", lazy="joined")