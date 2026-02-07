from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from app.schemas.todo import Todo, TodoCreate, TodoUpdate, TodoListResponse
from app.core.dependencies import get_todo_service, get_current_user
from app.services.todo_service import TodoService
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Create a new todo (requires authentication)"""
    return todo_service.create_todo(todo, owner_id=current_user.id)


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    is_done: Optional[bool] = Query(None, description="Filter by completion status"),
    q: Optional[str] = Query(None, description="Search by title or description"),
    sort: Optional[str] = Query(None, description="Sort by: created_at or -created_at"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Get user's todos with filtering, searching, sorting and pagination (requires authentication)"""
    return todo_service.get_todos(
        owner_id=current_user.id,
        is_done=is_done, 
        q=q, 
        sort=sort, 
        limit=limit, 
        offset=offset
    )


@router.get("/overdue", response_model=TodoListResponse)
async def get_overdue_todos(
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Get overdue todos (past due_date and not completed - requires authentication)"""
    return todo_service.get_overdue(
        owner_id=current_user.id,
        limit=limit,
        offset=offset
    )


@router.get("/today", response_model=TodoListResponse)
async def get_today_todos(
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Get today's todos (due_date is today and not completed - requires authentication)"""
    return todo_service.get_today(
        owner_id=current_user.id,
        limit=limit,
        offset=offset
    )


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Get a specific todo (requires authentication)"""
    todo = todo_service.get_todo(todo_id, owner_id=current_user.id)
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
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Update a todo (full update - requires authentication)"""
    updated_todo = todo_service.update_todo(todo_id, owner_id=current_user.id, todo_update=todo_update)
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
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Partial update todo (only update provided fields - requires authentication)"""
    updated_todo = todo_service.update_todo(todo_id, owner_id=current_user.id, todo_update=todo_update)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo


@router.post("/{todo_id}/complete", response_model=Todo)
async def mark_todo_complete(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Mark todo as complete (requires authentication)"""
    completed_todo = todo_service.mark_complete(todo_id, owner_id=current_user.id)
    if not completed_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return completed_todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service),
    current_user: User = Depends(get_current_user)
):
    """Delete a todo (requires authentication)"""
    success = todo_service.delete_todo(todo_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )