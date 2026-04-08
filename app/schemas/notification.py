from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.models.notification import NotificationStatus


class NotificationCreate(BaseModel):
    """Схема для создания уведомления"""
    
    recipient: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    channel: str = Field("email")


class NotificationResponse(BaseModel):
    """Схема ответа от API"""
    
    id: int
    recipient: str
    message: str
    channel: str
    status: NotificationStatus
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        orm_mode = True   # важно для Pydantic v1