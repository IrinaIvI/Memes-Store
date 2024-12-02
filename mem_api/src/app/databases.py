from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncGenerator

URL = "postgresql+asyncpg://postgres:password@localhost/mem_db"
engine = create_async_engine(url=URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session