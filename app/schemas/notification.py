from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.models.notification import NotificationStatus


class NotificationCreate(BaseModel):
    """Схема для создания уведомления с валидацией"""
    model_config = ConfigDict(from_attributes=True)

    recipient: str = Field(
        ..., 
        min_length=3, 
        max_length=255, 
        description="Email, телефон или username получателя"
    )
    message: str = Field(
        ..., 
        min_length=5, 
        max_length=1000, 
        description="Текст уведомления"
    )
    channel: str = Field(
        default="email", 
        pattern="^(email|sms|telegram)$",
        description="Канал отправки"
    )


class NotificationResponse(BaseModel):
    """Схема ответа"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipient: str
    message: str
    channel: str
    status: NotificationStatus
    created_at: datetime
    sent_at: Optional[datetime] = None