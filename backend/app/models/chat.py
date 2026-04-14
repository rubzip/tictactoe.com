from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.constants import Player, GameStatus, DifficultyMode


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(String, ForeignKey("games.room_id"), index=True, nullable=False)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    
    message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
