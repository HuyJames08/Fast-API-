from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    is_done: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None


class Todo(TodoBase):
    id: int
    
    class Config:
        from_attributes = True