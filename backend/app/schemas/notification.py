from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.notification import NotificationType


class NotificationBase(BaseModel):
    message: str
    type: NotificationType
    link_data: Optional[str] = None


class Notification(NotificationBase):
    id: int
    username: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationList(BaseModel):
    notifications: List[Notification]
