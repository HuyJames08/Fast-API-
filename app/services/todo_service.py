from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.todo import TodoCreate, TodoUpdate, Todo, TodoListResponse
from app.repositories.todo_repo import TodoRepository
from app.utils.pagination import paginate_list


class TodoService:
    """Business logic for todos with database"""
    
    def __init__(self, db: Session):
        self.repo = TodoRepository(db)
    
    def create_todo(self, todo: TodoCreate) -> Todo:
        """Create a new todo"""
        created_todo = self.repo.create(todo)
        return Todo.from_orm(created_todo)
    
    def get_todos(self, 
                 is_done: Optional[bool] = None, 
                 q: Optional[str] = None, 
                 sort: Optional[str] = None,
                 limit: int = 10, 
                 offset: int = 0) -> TodoListResponse:
        """Get todos with filtering, searching, sorting and pagination"""
        todos, total = self.repo.get_all(is_done=is_done, q=q, sort=sort, limit=limit, offset=offset)
        todo_objects = [Todo.from_orm(todo) for todo in todos]
        
        return TodoListResponse(
            items=todo_objects,
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID"""
        todo = self.repo.get_by_id(todo_id)
        if todo:
            return Todo.from_orm(todo)
        return None
    
    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update todo"""
        updated_todo = self.repo.update(todo_id, todo_update)
        if updated_todo:
            return Todo.from_orm(updated_todo)
        return None
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete todo"""
        return self.repo.delete(todo_id)
    
    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """Mark todo as complete"""
        completed_todo = self.repo.mark_complete(todo_id)
        if completed_todo:
            return Todo.from_orm(completed_todo)
        return None