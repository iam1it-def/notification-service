from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
import asyncio
import logging

from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate

logger = logging.getLogger(__name__)


async def create_notification(db: AsyncSession, notification_in: NotificationCreate):
    """Создать новое уведомление и запустить фоновую отправку"""
    db_notification = Notification(
        recipient=notification_in.recipient,
        message=notification_in.message,
        channel=notification_in.channel,
        status=NotificationStatus.PENDING,
        attempt=0
    )
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)

    # Запускаем фоновую отправку (имитация)
    asyncio.create_task(send_notification_background(db, db_notification.id))
    
    return db_notification


async def send_notification_background(db: AsyncSession, notification_id: int):
    """Фоновая задача имитации отправки уведомления"""
    await asyncio.sleep(2)  # имитация задержки отправки (2 секунды)

    try:
        # Обновляем статус на SENT
        result = await db.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(
                status=NotificationStatus.SENT,
                sent_at=datetime.utcnow(),
                attempt=Notification.attempt + 1
            )
        )
        await db.commit()
        
        logger.info(f"Уведомление #{notification_id} успешно отправлено")
        
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления #{notification_id}: {e}")
        # При ошибке можно поставить статус FAILED, но пока оставляем просто логи


async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список уведомлений"""
    result = await db.execute(
        select(Notification)
        .offset(skip)
        .limit(limit)
        .order_by(Notification.created_at.desc())
    )
    return result.scalars().all()