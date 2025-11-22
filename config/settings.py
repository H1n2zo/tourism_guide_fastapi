"""
Application Settings for Tourism Guide FastAPI
Loads configuration from .env file
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App Info
    APP_NAME: str = "Tourism Guide System"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    BASE_URL: str = "http://localhost:8000"
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:@localhost/tourism_guide"
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "tourism_guide"
    DB_PORT: int = 3306
    
    # Security
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Map Settings (FREE!)
    MAP_PROVIDER: str = "leaflet"
    MAP_DEFAULT_LAT: float = 11.0059
    MAP_DEFAULT_LNG: float = 124.6075
    MAP_DEFAULT_ZOOM: int = 13
    
    # Admin Defaults
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_EMAIL: str = "admin@tourismguide.com"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()