from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str | None = None


class User(UserBase):
    elo_rating: int = 1000
    is_active: bool = True

    played_games: int = 0
    won_games: int = 0
    lost_games: int = 0

    class Config:
        from_attributes = True
