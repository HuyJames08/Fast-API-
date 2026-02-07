from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from app.schemas.todo import Todo, TodoCreate, TodoUpdate, TodoListResponse
from app.core.dependencies import get_todo_service
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Create a new todo"""
    return todo_service.create_todo(todo)


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    is_done: Optional[bool] = Query(None, description="Filter by completion status"),
    q: Optional[str] = Query(None, description="Search by title or description"),
    sort: Optional[str] = Query(None, description="Sort by: created_at or -created_at"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    todo_service: TodoService = Depends(get_todo_service)
):
    """Get todos with filtering, searching, sorting and pagination"""
    return todo_service.get_todos(
        is_done=is_done, 
        q=q, 
        sort=sort, 
        limit=limit, 
        offset=offset
    )


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Get a specific todo"""
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Update a todo (full update)"""
    updated_todo = todo_service.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.patch("/{todo_id}", response_model=Todo)
async def partial_update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Partial update todo (only update provided fields)"""
    updated_todo = todo_service.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.post("/{todo_id}/complete", response_model=Todo)
async def mark_todo_complete(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Mark todo as complete"""
    completed_todo = todo_service.mark_complete(todo_id)
    if not completed_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return completed_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Delete a todo"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )