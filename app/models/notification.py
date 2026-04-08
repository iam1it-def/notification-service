from datetime import datetime
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


# типы статусов 
class NotificationStatus(str, enum.Enum):
    PENDING = "pending"      # в очереди
    SENT = "sent"            # отправлено
    FAILED = "failed"        # ошибка


class Notification(Base):
    """Модель уведомления в базе данных"""
    
    __tablename__ = "notifications"   # имя таблицы в PostgreSQL
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)   # кому отправить
    message: Mapped[str] = mapped_column(Text, nullable=False)            # текст сообщения
    channel: Mapped[str] = mapped_column(String(50), default="email")     # email, sms, telegram и т.д.
    
    status: Mapped[NotificationStatus] = mapped_column(
        SQLEnum(NotificationStatus), 
        default=NotificationStatus.PENDING
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)