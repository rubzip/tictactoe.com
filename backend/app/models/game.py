from sqlalchemy import Column, Integer, String, Boolean, JSON, Enum, DateTime, ForeignKey
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

    # Player X
    player_x_username = Column(String, ForeignKey("users.username"), nullable=True)
    player_x_avatar = Column(String, nullable=True)
    
    # Player O
    player_o_username = Column(String, ForeignKey("users.username"), nullable=True)
    player_o_avatar = Column(String, nullable=True)
    
    # AI Game specific fields
    ai_player_x_difficulty = Column(Enum(DifficultyMode), nullable=True)
    ai_player_o_difficulty = Column(Enum(DifficultyMode), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
