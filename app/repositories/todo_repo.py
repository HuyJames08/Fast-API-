from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.models.todo import Todo as TodoModel
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """Todo repository for database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, todo: TodoCreate, owner_id: int) -> TodoModel:
        """Create a new todo"""
        db_todo = TodoModel(
            title=todo.title,
            description=todo.description,
            is_done=todo.is_done,
            owner_id=owner_id
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def get_all(self, 
               owner_id: int,
               is_done: Optional[bool] = None, 
               q: Optional[str] = None, 
               sort: Optional[str] = None,
               limit: int = 10,
               offset: int = 0) -> tuple[List[TodoModel], int]:
        """Get todos for user with filtering, searching and sorting. Returns (items, total)"""
        query = self.db.query(TodoModel)
        
        # Filter by owner
        query = query.filter(TodoModel.owner_id == owner_id)
        
        # Filter by is_done status
        if is_done is not None:
            query = query.filter(TodoModel.is_done == is_done)
        
        # Search by title or description keyword
        if q:
            query = query.filter(
                or_(
                    TodoModel.title.ilike(f"%{q}%"),
                    TodoModel.description.ilike(f"%{q}%")
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Sort by created_at
        if sort == "created_at":
            query = query.order_by(TodoModel.created_at)
        elif sort == "-created_at":
            query = query.order_by(desc(TodoModel.created_at))
        else:
            # Default: newest first
            query = query.order_by(desc(TodoModel.created_at))
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        return query.all(), total
    
    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Get todo by ID and verify ownership"""
        return self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id
        ).first()
    
    def update(self, todo_id: int, todo_update: TodoUpdate, owner_id: int) -> Optional[TodoModel]:
        """Update todo - verify ownership"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if not db_todo:
            return None
        
        if todo_update.title is not None:
            db_todo.title = todo_update.title
        if todo_update.description is not None:
            db_todo.description = todo_update.description
        if todo_update.is_done is not None:
            db_todo.is_done = todo_update.is_done
        
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def delete(self, todo_id: int, owner_id: int) -> bool:
        """Delete todo - verify ownership"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if not db_todo:
            return False
        
        self.db.delete(db_todo)
        self.db.commit()
        return True
    
    def mark_complete(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Mark todo as complete - verify ownership"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if not db_todo:
            return None
        
        db_todo.is_done = True
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo