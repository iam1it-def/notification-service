from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.config import settings
from app.database import get_db
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.crud.notification import create_notification, get_notifications

app = FastAPI(
    title="Notification Service (для Voxys)",
    description="Простой бэкенд сервис уведомлений — проект для портфолио",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Сервис уведомлений запущен! Открой /docs для тестирования"}


@app.post("/notifications/", response_model=NotificationResponse)
async def create_new_notification(
    notification_in: NotificationCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Создать новое уведомление"""
    notification = await create_notification(db, notification_in)
    return notification


@app.get("/notifications/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Получить список уведомлений"""
    notifications = await get_notifications(db, skip=skip, limit=limit)
    return notifications


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)