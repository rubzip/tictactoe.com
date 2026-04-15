# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    avatar_url = Column(String, nullable=True)
    hashed_password = Column(String)
    
    # Atributos de juego basados en tus esquemas
    elo_rating = Column(Float, default=1000.0)
    is_active = Column(Boolean, default=True)
    
    # Estadísticas
    played_games = Column(Integer, default=0)
    won_games = Column(Integer, default=0)
    lost_games = Column(Integer, default=0)
