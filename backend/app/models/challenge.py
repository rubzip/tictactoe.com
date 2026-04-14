from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.constants import ChallengeStatus



class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    challenger_username = Column(String, ForeignKey("users.username"))
    challenged_username = Column(String, ForeignKey("users.username"))
    
    room_id = Column(String, unique=True, index=True)
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    challenger = relationship("User", foreign_keys=[challenger_username])
    challenged = relationship("User", foreign_keys=[challenged_username])
