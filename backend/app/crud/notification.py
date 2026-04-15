from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType


from app.schemas.notification import NotificationCreate


def create_notification(
    db: Session, 
    notification_in: NotificationCreate
) -> Notification:
    db_notification = Notification(
        username=notification_in.username,
        message=notification_in.message,
        type=notification_in.type,
        link_data=notification_in.link_data
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_user_notifications(db: Session, username: str, limit: int = 50) -> list[Notification]:
    return db.query(Notification).filter(
        Notification.username == username
    ).order_by(Notification.created_at.desc()).limit(limit).all()


def mark_as_read(db: Session, notification_id: int, username: str) -> bool:
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.username == username
    ).first()
    if db_notification:
        db_notification.is_read = True
        db.commit()
        return True
    return False
