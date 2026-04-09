# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Atributos de juego basados en tus esquemas
    elo_rating = Column(Integer, default=1000)
    is_active = Column(Boolean, default=True)
    
    # Estadísticas
    played_games = Column(Integer, default=0)
    won_games = Column(Integer, default=0)
    lost_games = Column(Integer, default=0)
