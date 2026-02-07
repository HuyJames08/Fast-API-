from sqlalchemy import Column, String, Boolean, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, BaseModel
from datetime import datetime


class Todo(BaseModel):
    """Todo ORM Model with deadline and tags"""
    __tablename__ = "todos"
    
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, index=True)
    due_date = Column(DateTime, nullable=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationships
    owner = relationship("User", lazy="joined")
    tags = relationship("Tag", secondary="todo_tag", back_populates="todos")