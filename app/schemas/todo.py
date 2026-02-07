from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagSchema(BaseModel):
    """Tag schema for response"""
    id: int
    name: str
    
    class Config:
        from_attributes = True


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, 
                      description="Todo title must be 3-100 characters")
    description: Optional[str] = Field(None, description="Optional description")
    is_done: bool = False
    due_date: Optional[datetime] = Field(None, description="Deadline for this todo")


class TodoCreate(TodoBase):
    tags: Optional[List[str]] = Field(None, description="List of tag names")


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, 
                               description="Todo title must be 3-100 characters")
    description: Optional[str] = Field(None, description="Optional description")
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = Field(None, description="Deadline for this todo")
    tags: Optional[List[str]] = Field(None, description="List of tag names")


class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagSchema] = Field(default_factory=list, description="Tags for this todo")
    
    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    items: List[Todo]
    total: int
    limit: int
    offset: int