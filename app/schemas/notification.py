from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.models.notification import NotificationStatus


class NotificationCreate(BaseModel):
    """Схема для создания нового уведомления (что присылает пользователь)"""
    
    recipient: str = Field(..., min_length=1, max_length=255, description="Кому отправить (email, телефон и т.д.)")
    message: str = Field(..., min_length=1, description="Текст уведомления")
    channel: str = Field("email", pattern="^(email|sms|telegram)$", description="Канал отправки")


class NotificationResponse(BaseModel):
    """Схема для ответа пользователю (что возвращает API)"""
    
    id: int
    recipient: str
    message: str
    channel: str
    status: NotificationStatus
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True   # позволяет работать с объектами из базы данных