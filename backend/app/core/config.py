from pydantic_settings import BaseSettings  # Changed from pydantic import
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+psycopg2://test_admin:ilikec@123@localhost:5432/datasage_db"
    
    # Security
    secret_key: str = 6253434262524328352838362
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # API Settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True
    
    # Frontend
    frontend_url: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"

settings = Settings()
