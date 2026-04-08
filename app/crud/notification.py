from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate


async def create_notification(db: AsyncSession, notification: NotificationCreate):
    """Создать новое уведомление в базе"""
    db_notification = Notification(
        recipient=notification.recipient,
        message=notification.message,
        channel=notification.channel,
        status=NotificationStatus.PENDING
    )
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification


async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить список уведомлений"""
    result = await db.execute(
        select(Notification).offset(skip).limit(limit)
    )
    return result.scalars().all()