from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.todo import Todo, TodoCreate, TodoUpdate
from app.services.todo_service import todo_service

router = APIRouter()


@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    return todo_service.create_todo(todo)


@router.get("/todos", response_model=List[Todo])
async def get_todos():
    """Get all todos"""
    return todo_service.get_todos()


@router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get todo by ID"""
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update todo"""
    updated_todo = todo_service.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """Delete todo"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )