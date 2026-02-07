from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


# Association table for many-to-many relationship between todos and tags
todo_tag_association = Table(
    'todo_tag',
    Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Tag(Base):
    """Tag model for categorizing todos"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relationship
    todos = relationship("Todo", secondary=todo_tag_association, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"