from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:@localhost/tourism_guide"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-09af9s0d8f7asd098f7a"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "Tourism Guide System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif", "webp"}
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Create upload directories
os.makedirs(os.path.join(settings.UPLOAD_DIR, "destinations"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "categories"), exist_ok=True)
