# Level 6: Advanced Features - Tags, Deadlines & Smart Filtering - COMPLETE ✓

## Implementation Summary

Level 6 adds advanced todo management features: tags for categorization, deadline support, and smart filtering to identify overdue and today's tasks.

### 🎯 Key Features Implemented

#### 1. Tag System
- **Tag Model** (`app/models/tag.py`)
  - Unique tag names (indexed)
  - Many-to-many relationship with todos
  - Shared across all todos (single "work" tag used by multiple todos)

- **Tag Schemas** (`app/schemas/tag.py`)
  - TagBase, TagCreate, Tag, TagResponse

- **Todo-Tag Association**
  - Association table: `todo_tag`
  - Automatic tag creation if not exists
  - Tag reuse across todos

#### 2. Deadline Support
- **due_date Field**
  - DateTime field in Todo model (nullable, indexed)
  - Can be in past, present, or future
  - Used for filtering and sorting

- **Deadline in Schemas**
  - TodoBase includes optional due_date
  - TodoCreate supports setting deadline on creation
  - TodoUpdate can modify deadline

#### 3. Smart Todo Filtering

#### GET /api/v1/todos/overdue
- Returns incomplete todos with due_date in the past
- Sorted by due_date (earliest first)
- Filtered by current user owner_id
- Supports pagination (limit, offset)

#### GET /api/v1/todos/today
- Returns incomplete todos with due_date for today
- Compares dates (ignores time component)
- Filtered by current user owner_id
- Supports pagination

#### 4. Enhanced Todo Operations
- **Create** (`POST /todos`)
  - Accept due_date and tags list
  - Auto-create tags if not exist
  - Tags assigned after todo creation

- **Update** (`PUT/PATCH /todos/{id}`)
  - Update due_date
  - Replace tags with new list
  - Verify ownership

### 📊 Database Schema

#### Tags Table
```
id | name (unique, indexed)
```

#### Todo_Tag Association Table
```
todo_id | tag_id (composite primary key)
```
- ON DELETE CASCADE for both foreign keys

#### Updated Todos Table
```
id | title | description | is_done | due_date | owner_id | created_at | updated_at
```
- Indexed: title, is_done, due_date, owner_id

### 🏗️ Architecture

#### Repository Pattern
```
TodoRepository:
  - get_all() - Get todos with filters
  - get_overdue() - Todos past due_date, not done
  - get_today() - Todos due today, not done
  - create() - Create with tags (auto-create tags)
  - update() - Update tags and fields
```

#### Service Layer
```
TodoService:
  - get_overdue(owner_id, limit, offset) -> TodoListResponse
  - get_today(owner_id, limit, offset) -> TodoListResponse
  - Delegates to repository
```

#### API Endpoints
```
POST   /api/v1/todos
GET    /api/v1/todos
GET    /api/v1/todos/today
GET    /api/v1/todos/overdue
GET    /api/v1/todos/{id}
PUT    /api/v1/todos/{id}
PATCH  /api/v1/todos/{id}
POST   /api/v1/todos/{id}/complete
DELETE /api/v1/todos/{id}
```

### ✅ Test Results

All Level 6 features tested successfully:

**Test 1**: Create todo with tags (tomorrow)
- Status: 201 Created
- Tags created: 2 (work, urgent)

**Test 2**: Create todo for today
- Status: 201 Created
- Tags created: 2 (meeting, important)

**Test 3**: Create overdue todo (yesterday)
- Status: 201 Created
- Tags created: 1 (review)

**Test 4**: Get today's todos
- Status: 200 OK
- Returned: 1 todo (Team meeting)
- Correct filtering by due_date

**Test 5**: Get overdue todos
- Status: 200 OK
- Returned: 1 todo (Review documents)
- Correct filtering by past due_date

**Test 6**: Get all todos
- Status: 200 OK
- Returned: 3 todos total
- All with tags populated

**Test 7**: Update todo with new tags
- Status: 200 OK
- Tags updated: 3 (work, urgent, priority)
- New tag created automatically

**Test 8**: Verify tag sharing
- Unique tags across todos: 5
- Tags properly shared and reused

### 💾 Data Example

```json
{
  "title": "Complete project",
  "description": "Finish the project",
  "is_done": false,
  "due_date": "2026-02-08T12:06:46.695698",
  "tags": [
    {"id": 1, "name": "work"},
    {"id": 2, "name": "urgent"}
  ],
  "id": 1,
  "created_at": "2026-02-07T05:06:48.726427",
  "updated_at": "2026-02-07T05:06:48.726427"
}
```

### 🔧 Technologies

```
SQLAlchemy:
  - Many-to-many relationship
  - Association table with cascade delete
  - DateTime queries for filtering
  
FastAPI:
  - Multiple filter endpoints
  - Pagination consistency
  - Dependency injection

Pydantic:
  - DateTime validation
  - List field for tags
  - Nested schema serialization
```

### 📁 Files Created/Modified

**New Files:**
- `app/models/tag.py` - Tag ORM model
- `app/schemas/tag.py` - Tag schemas
- `test_level6.py` - Comprehensive Level 6 tests

**Modified Files:**
- `app/models/todo.py` - Added due_date and tags relationship
- `app/models/__init__.py` - Export Tag model
- `app/schemas/todo.py` - Added due_date and tags to schemas
- `app/repositories/todo_repo.py` - Added tag handling and filter methods
- `app/services/todo_service.py` - Added overdue/today methods
- `app/routers/todos.py` - Added /overdue and /today endpoints
- `app/main.py` - Import Tag model

### 🚀 Running Level 6

```bash
# Start server
python -m uvicorn app.main:app --reload --port 8000

# Run tests
python test_level6.py

# API Documentation
http://localhost:8000/api/v1/docs
```

### 📝 Usage Examples

**Create todo with tags and deadline:**
```bash
POST /api/v1/todos
{
  "title": "Project deadline",
  "due_date": "2026-02-10T17:00:00",
  "tags": ["work", "urgent"]
}
```

**Get today's todos:**
```bash
GET /api/v1/todos/today?limit=10&offset=0
```

**Get overdue todos:**
```bash
GET /api/v1/todos/overdue?limit=10&offset=0
```

**Update todo with new tags:**
```bash
PATCH /api/v1/todos/1
{
  "tags": ["work", "urgent", "priority"]
}
```

### ✨ Smart Features

1. **Auto Tag Creation**: Tags are automatically created if they don't exist
2. **Tag Reuse**: Multiple todos can share the same tags
3. **User Isolation**: Overdue/today endpoints respect user ownership
4. **Pagination**: All filtered endpoints support limit/offset
5. **Sorting**: Overdue/today todos sorted by due_date
6. **Date Filtering**: Overdue excludes time, today uses date boundaries

### 🔒 Security

- All endpoints require authentication (JWT bearer token)
- Overdue/today endpoints filter by owner_id
- Users cannot see other users' todos
- Tag names are unique but shared across all users

### 🎯 Next Steps (Levels 7-8)

Potential future enhancements:
- Recurring todos (daily, weekly, monthly)
- Priorities (high, medium, low)
- Categories vs tags
- Reminders/notifications
- Sharing todos with other users
- Collaborative todos
- Due time notifications

---

**Level 6 Status**: ✅ COMPLETE - All advanced features tested and verified. Tags, deadlines, overdue filtering, and today's task filtering all working correctly!
