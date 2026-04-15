from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.users import User
from app.core.exceptions import NotificationNotFoundException
from app.schemas.notification import Notification, NotificationList, NotificationUpdate

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.get("/", response_model=NotificationList)
def read_notifications(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all notifications for the current user.
    """
    notifications = crud.notification.get_user_notifications(db, username=current_user.username, limit=limit)
    return NotificationList(notifications=notifications)


@router.patch("/{notification_id}/read", response_model=dict)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a notification as read.
    """
    # Verify ownership indirectly by getting it first? 
    # Or just let CRUD handle it but it's better to check.
    success = crud.notification.mark_as_read(db, notification_id=notification_id, username=current_user.username)
    if not success:
        raise NotificationNotFoundException(notification_id)
    return {"status": "success"}
