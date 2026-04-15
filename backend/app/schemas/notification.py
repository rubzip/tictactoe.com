from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.notification import NotificationType


class NotificationBase(BaseModel):
    message: str
    type: NotificationType
    link_data: Optional[str] = None


class NotificationCreate(NotificationBase):
    username: str


class Notification(NotificationCreate):
    id: int
    is_read: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationList(BaseModel):
    notifications: List[Notification]
