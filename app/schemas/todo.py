from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TodoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, 
                      description="Todo title must be 3-100 characters")
    description: Optional[str] = Field(None, description="Optional description")
    is_done: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100, 
                               description="Todo title must be 3-100 characters")
    description: Optional[str] = Field(None, description="Optional description")
    is_done: Optional[bool] = None


class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    items: List[Todo]
    total: int
    limit: int
    offset: int