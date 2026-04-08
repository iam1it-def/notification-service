import asyncio
from app.database import engine
from app.models.notification import Base

async def init_db():
    print("🔄 Создаём таблицы в базе данных...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы успешно созданы! (включая поле 'attempt')")

if __name__ == "__main__":
    asyncio.run(init_db())