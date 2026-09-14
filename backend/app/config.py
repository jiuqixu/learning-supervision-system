from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "Learning Supervision System"
    debug: bool = True
    log_level: str = "INFO"
    
    # 数据库配置
    database_url: str = "postgresql://postgres:password@localhost:5432/learning_db"
    redis_url: str = "redis://localhost:6379"
    
    # JWT配置
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS配置
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
