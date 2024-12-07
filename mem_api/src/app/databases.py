from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator
from app.config import DATABASE_URL

engine = create_async_engine(url="postgresql+asyncpg://postgres:password@host.docker.internal:5432/mem_db", echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессии."""
    async with async_session() as session:
        yield session