from typing import List, Optional
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """In-memory todo repository for Level 1"""
    
    def __init__(self):
        self._todos: List[dict] = []
        self._next_id = 1
    
    def create(self, todo: TodoCreate) -> dict:
        """Create a new todo"""
        new_todo = {
            "id": self._next_id,
            "title": todo.title,
            "is_done": todo.is_done
        }
        self._todos.append(new_todo)
        self._next_id += 1
        return new_todo
    
    def get_all(self) -> List[dict]:
        """Get all todos"""
        return self._todos
    
    def get_by_id(self, todo_id: int) -> Optional[dict]:
        """Get todo by ID"""
        for todo in self._todos:
            if todo["id"] == todo_id:
                return todo
        return None
    
    def update(self, todo_id: int, todo_update: TodoUpdate) -> Optional[dict]:
        """Update todo"""
        todo = self.get_by_id(todo_id)
        if not todo:
            return None
        
        if todo_update.title is not None:
            todo["title"] = todo_update.title
        if todo_update.is_done is not None:
            todo["is_done"] = todo_update.is_done
            
        return todo
    
    def delete(self, todo_id: int) -> bool:
        """Delete todo"""
        todo = self.get_by_id(todo_id)
        if not todo:
            return False
        
        self._todos.remove(todo)
        return True


# Global instance for Level 1
todo_repo = TodoRepository()