from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.models.todo import Todo  # Import models to register them
from app.models.user import User  # Import User model to register it
from app.routers import health, todos, auth

# Create all tables on startup
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A professional ToDo API built with FastAPI",
    version=settings.version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 Routes
api_v1_prefix = settings.api_v1_prefix
app.include_router(health.router, prefix=api_v1_prefix)
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(todos.router, prefix=api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to ToDo API",
        "version": settings.version,
        "environment": settings.environment,
        "docs": f"{settings.api_v1_prefix}/docs",
        "redoc": f"{settings.api_v1_prefix}/redoc"
    }