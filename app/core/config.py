from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "ToDo API"
    debug: bool = True
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"


settings = Settings()