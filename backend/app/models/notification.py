from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class NotificationType(str, enum.Enum):
    INFO = "INFO"
    CHALLENGE = "CHALLENGE"
    MATCH_FOUND = "MATCH_FOUND"
    SYSTEM = "SYSTEM"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False, index=True)
    message = Column(String, nullable=False)
    type = Column(Enum(NotificationType), default=NotificationType.INFO)
    is_read = Column(Boolean, default=False)
    
    # Extra data for links (e.g. room_id or challenge_id)
    link_data = Column(String, nullable=True) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
