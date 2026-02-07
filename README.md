# ToDo API - FastAPI Project

## 📋 Project Structure

```
fastapi-todo/
├── app/
│   ├── main.py                 # Clean main entry point
│   ├── core/
│   │   ├── config.py          # Settings from environment
│   │   ├── database.py        # DB config (Level 4)
│   │   ├── security.py        # Auth (Level 5)
│   │   └── dependencies.py    # Dependency injection
│   ├── models/                # ORM models (Level 4+)
│   ├── schemas/               # Pydantic schemas
│   ├── repositories/          # Data access layer
│   ├── services/              # Business logic layer
│   ├── routers/               # API endpoints
│   └── utils/                 # Helper functions
├── alembic/                   # Database migrations (Level 4)
├── tests/                     # Test suite (Level 7)
├── .env                       # Environment variables
├── requirements.txt           # Dependencies
└── README.md
```

## 🚀 Cách Chạy

### Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### Chạy Server
```bash
uvicorn app.main:app --reload
```

Server sẽ chạy tại: `http://localhost:8000`

## 📚 API Documentation

- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

## 📝 Levels

### Cấp 0 ✅ - Làm quen FastAPI (Hello To-Do)
- ✅ GET /health → {"status": "ok"}
- ✅ GET / → Greeting message

### Cấp 1 ✅ - CRUD cơ bản (dữ liệu trong RAM)
- ✅ POST /api/v1/todos - Tạo
- ✅ GET /api/v1/todos - Lấy danh sách
- ✅ GET /api/v1/todos/{id} - Lấy chi tiết
- ✅ PUT /api/v1/todos/{id} - Cập nhật
- ✅ DELETE /api/v1/todos/{id} - Xóa
- ✅ Validation Pydantic
- ✅ Error handling 404

### Cấp 2 ✅ - Validation "xịn" + filter/sort/pagination
- ✅ Title validation (3-100 chars)
- ✅ Filter: ?is_done=true/false
- ✅ Search: ?q=keyword
- ✅ Sort: ?sort=created_at or -created_at
- ✅ Pagination: ?limit=10&offset=0

### Cấp 3 ✅ - Tách tầng + Config chuẩn
- ✅ APIRouter với prefix /api/v1
- ✅ Tách: routers/, services/, repositories/
- ✅ Config via pydantic-settings (.env)
- ✅ Main.py sạch (không logic)
- ✅ CORS middleware

### Cấp 4 ⏳ - Database + ORM
- [ ] SQLAlchemy ORM
- [ ] Alembic migrations
- [ ] PostgreSQL/SQLite
- [ ] PATCH /todos/{id} partial update

### Cấp 5 ⏳ - Authentication + User
- [ ] JWT tokens
- [ ] User management
- [ ] Password hashing
- [ ] Owner check

### Cấp 6 ⏳ - Advanced Features
- [ ] Tags
- [ ] Deadline (due_date)
- [ ] GET /todos/overdue
- [ ] GET /todos/today

### Cấp 7 ⏳ - Testing + Deploy
- [ ] pytest + TestClient
- [ ] Dockerfile
- [ ] docker-compose
- [ ] CI/CD

## Git Branches

```bash
# Checkout specific level
git checkout level-0
git checkout level-4
git checkout level-5
git checkout level-6
git checkout main  # Latest version
```

## 📧 Environment Variables (.env)

```env
APP_NAME=ToDo API
DEBUG=true
VERSION=1.0.0
API_V1_PREFIX=/api/v1
ENVIRONMENT=development
```
# Fast-API-
