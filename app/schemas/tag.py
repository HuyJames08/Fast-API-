from pydantic import BaseModel, Field
from typing import Optional


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True


class TagResponse(Tag):
    """Response schema for tag"""
    pass