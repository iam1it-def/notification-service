import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.config import settings
from app.database import get_db
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.crud.notification import create_notification, get_notifications

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Notification Service",
    description="Простой сервис отправки уведомлений — проект для портфолио",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальный обработчик ошибок
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Неожиданная ошибка: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Произошла внутренняя ошибка сервера. Попробуйте позже."}
    )

@app.get("/")
async def root():
    return {"message": "Notification Service работает!"}


@app.post("/notifications/", response_model=NotificationResponse)
async def create_new_notification(
    notification_in: NotificationCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Создать новое уведомление"""
    try:
        notification = await create_notification(db, notification_in)
        logger.info(f"Создано новое уведомление для {notification_in.recipient}")
        return notification
    except Exception as e:
        logger.error(f"Ошибка при создании уведомления: {e}")
        raise HTTPException(status_code=500, detail="Не удалось создать уведомление")


@app.get("/notifications/", response_model=List[NotificationResponse])
async def list_notifications(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех уведомлений"""
    try:
        notifications = await get_notifications(db, skip=skip, limit=limit)
        logger.info(f"Возвращено {len(notifications)} уведомлений")
        return notifications
    except Exception as e:
        logger.error(f"Ошибка при получении списка уведомлений: {e}")
        raise HTTPException(status_code=500, detail="Не удалось получить список уведомлений")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)