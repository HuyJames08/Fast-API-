# ToDo API - FastAPI Project

## Cấp 0 - Làm quen FastAPI (Hello To-Do)

### Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Chạy server:
```bash
uvicorn main:app --reload
```

### Endpoints

- `GET /` - Greeting message
- `GET /health` - Health check

### Test

Mở browser và truy cập:
- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/docs (Swagger UI)

## Git commits theo cấp độ

- Cấp 0: Basic FastAPI setup
- Cấp 4: Database integration
- Cấp 5: Authentication  
- Cấp 6: Advanced features
- end: Final version