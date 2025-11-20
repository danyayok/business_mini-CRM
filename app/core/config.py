from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://user:pass@localhost:5432/crm"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    redis_url: str = "redis://localhost:6379"
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    environment: str = "development"
    class Config:
        env_file = ".env"


settings = Settings()