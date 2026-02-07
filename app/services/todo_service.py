from typing import List, Optional
from app.schemas.todo import Todo, TodoCreate, TodoUpdate
from app.repositories.todo_repo import todo_repo


class TodoService:
    """Todo service for business logic"""
    
    def __init__(self):
        self.repo = todo_repo
    
    def create_todo(self, todo: TodoCreate) -> Todo:
        """Create a new todo"""
        created_todo = self.repo.create(todo)
        return Todo(**created_todo)
    
    def get_todos(self) -> List[Todo]:
        """Get all todos"""
        todos = self.repo.get_all()
        return [Todo(**todo) for todo in todos]
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID"""
        todo = self.repo.get_by_id(todo_id)
        if todo:
            return Todo(**todo)
        return None
    
    def update_todo(self, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """Update todo"""
        updated_todo = self.repo.update(todo_id, todo_update)
        if updated_todo:
            return Todo(**updated_todo)
        return None
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete todo"""
        return self.repo.delete(todo_id)


# Global instance
todo_service = TodoService()