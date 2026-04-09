from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.constants import Player, GameStatus, DifficultyMode


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, unique=True, index=True, nullable=False)
    
    # Board state stored as JSON (List[List[str]])
    board = Column(JSON, nullable=False)
    
    turn = Column(Enum(Player), default=Player.X)
    status = Column(Enum(GameStatus), default=GameStatus.KEEP_PLAYING)
    
    # Winning line coordinates as JSON (List[tuple[int, int]])
    win_line = Column(JSON, default=list)
    
    # AI Game specific fields
    is_ai_game = Column(Boolean, default=False)
    ai_difficulty = Column(Enum(DifficultyMode), nullable=True)
    ai_player = Column(Enum(Player), default=Player.O)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
