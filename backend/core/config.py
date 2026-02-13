"""
Configuration settings for the Todo application
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/todo_app"
    neon_database_url: Optional[str] = None

    # Auth settings
    better_auth_secret: str = "your-better-auth-secret-key-here"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App settings
    app_name: str = "Todo Application"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    model_config = {"env_file": ".env"}


settings = Settings()