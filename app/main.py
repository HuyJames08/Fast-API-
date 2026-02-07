from fastapi import FastAPI
from app.routers import health, todos

app = FastAPI(
    title="ToDo API",
    description="A simple ToDo API built with FastAPI",
    version="1.0.0"
)

# Include routers
app.include_router(health.router)
app.include_router(todos.router)
app.include_router(todos.router)


@app.get("/")
async def root():
    """Root endpoint with greeting"""
    return {"message": "Hello World! Welcome to ToDo API"}