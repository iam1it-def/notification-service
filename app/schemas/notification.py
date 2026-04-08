from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.models.notification import NotificationStatus


class NotificationCreate(BaseModel):
    """Схема для создания нового уведомления"""
    model_config = ConfigDict(from_attributes=True)

    recipient: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    channel: str = Field(default="email")


class NotificationResponse(BaseModel):
    """Схема ответа API"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipient: str
    message: str
    channel: str
    status: NotificationStatus
    created_at: datetime
    sent_at: Optional[datetime] = None