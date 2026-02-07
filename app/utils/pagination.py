from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int


class PaginationParams:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = max(1, min(limit, 100))  # Limit between 1-100
        self.offset = max(0, offset)  # Offset >= 0


def paginate_list(items: List[T], limit: int = 10, offset: int = 0) -> PaginatedResponse[T]:
    """Paginate a list of items"""
    params = PaginationParams(limit, offset)
    total = len(items)
    start = params.offset
    end = start + params.limit
    paginated_items = items[start:end]
    
    return PaginatedResponse(
        items=paginated_items,
        total=total,
        limit=params.limit,
        offset=params.offset
    )