from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех таблиц в базе данных"""
    pass


# движок для подключения к SQLite
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,                    # SQL-запросы в консоли 
    connect_args={"check_same_thread": False}  # важно для SQLite
)


# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session