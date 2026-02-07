from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App configuration
    app_name: str = "ToDo API"
    debug: bool = True
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    
    # Environment
    environment: str = "development"
    
    # Database (placeholder for Level 4)
    database_url: Optional[str] = None
    
    # JWT Configuration
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()