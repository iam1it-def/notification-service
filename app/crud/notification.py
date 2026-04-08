from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate


async def create_notification(db: AsyncSession, notification_in: NotificationCreate):
    """Создать новое уведомление в базе данных"""
    db_notification = Notification(
        recipient=notification_in.recipient,
        message=notification_in.message,
        channel=notification_in.channel,
        status=NotificationStatus.PENDING
    )
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification


async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список всех уведомлений"""
    result = await db.execute(
        select(Notification).offset(skip).limit(limit).order_by(Notification.created_at.desc())
    )
    return result.scalars().all()