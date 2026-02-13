"""
Database session setup for the Todo application
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from core.config import settings
from sqlmodel import SQLModel


# Create async engine with connection pooling
# For Neon PostgreSQL, using standard asyncpg format
engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session
    """
    async with AsyncSession(engine) as session:
        yield session