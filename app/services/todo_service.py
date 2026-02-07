from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.todo import TodoCreate, TodoUpdate, Todo, TodoListResponse
from app.repositories.todo_repo import TodoRepository
from app.utils.pagination import paginate_list


class TodoService:
    """Business logic for todos with database"""
    
    def __init__(self, db: Session):
        self.repo = TodoRepository(db)
    
    def create_todo(self, todo: TodoCreate, owner_id: int) -> Todo:
        """Create a new todo for the current user"""
        created_todo = self.repo.create(todo, owner_id=owner_id)
        return Todo.from_orm(created_todo)
    
    def get_todos(self, 
                 owner_id: int,
                 is_done: Optional[bool] = None, 
                 q: Optional[str] = None, 
                 sort: Optional[str] = None,
                 limit: int = 10, 
                 offset: int = 0) -> TodoListResponse:
        """Get todos for the current user with filtering, searching, sorting and pagination"""
        todos, total = self.repo.get_all(owner_id=owner_id, is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)
        todo_objects = [Todo.from_orm(todo) for todo in todos]
        
        return TodoListResponse(
            items=todo_objects,
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_todo(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """Get todo by ID - verify ownership"""
        todo = self.repo.get_by_id(todo_id, owner_id=owner_id)
        if todo:
            return Todo.from_orm(todo)
        return None
    
    def update_todo(self, todo_id: int, owner_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update todo - verify ownership"""
        updated_todo = self.repo.update(todo_id, todo_update, owner_id=owner_id)
        if updated_todo:
            return Todo.from_orm(updated_todo)
        return None
    
    def delete_todo(self, todo_id: int, owner_id: int) -> bool:
        """Delete todo - verify ownership"""
        return self.repo.delete(todo_id, owner_id=owner_id)
    
    def mark_complete(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """Mark todo as complete - verify ownership"""
        completed_todo = self.repo.mark_complete(todo_id, owner_id=owner_id)
        if completed_todo:
            return Todo.from_orm(completed_todo)
        return None
    
    def get_overdue(self, owner_id: int, limit: int = 10, offset: int = 0) -> TodoListResponse:
        """Get overdue todos for the current user"""
        todos, total = self.repo.get_overdue(owner_id=owner_id, limit=limit, offset=offset)
        todo_objects = [Todo.from_orm(todo) for todo in todos]
        
        return TodoListResponse(
            items=todo_objects,
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_today(self, owner_id: int, limit: int = 10, offset: int = 0) -> TodoListResponse:
        """Get today's todos for the current user"""
        todos, total = self.repo.get_today(owner_id=owner_id, limit=limit, offset=offset)
        todo_objects = [Todo.from_orm(todo) for todo in todos]
        
        return TodoListResponse(
            items=todo_objects,
            total=total,
            limit=limit,
            offset=offset
        )