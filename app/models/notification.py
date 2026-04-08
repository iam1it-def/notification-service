from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
import enum
from typing import Optional

from app.database import Base


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Notification(Base):
    """Модель уведомления"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    
    recipient = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(String(50), default="email")
    
    status = Column(SQLEnum(NotificationStatus), default=NotificationStatus.PENDING)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sent_at = Column(DateTime, nullable=True)