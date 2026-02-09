from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses .env file in development.
    """
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PROJECT_NAME: str = "School Management System"
    VERSION: str = "1.0.0"
    
    # CORS - Allow frontend to connect
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3080",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3080",
        "http://127.0.0.1:8000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """
    Cache settings so we don't reload .env file on every request.
    This is a performance optimization.
    """
    return Settings()

# Usage: from app.config import get_settings
# settings = get_settings()