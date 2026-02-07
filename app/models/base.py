from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base as sql_declarative_base
from datetime import datetime

Base = sql_declarative_base()


class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)