from typing import Any
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: str
    avatar_url: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., max_length=72)


class UserChangePassword(BaseModel):
    password: str = Field(..., max_length=72)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, max_length=72, min_length=8)
    avatar_url: str | None = None


class User(UserBase):
    elo_rating: int = 1000
    is_active: bool = True

    played_games: int = 0
    won_games: int = 0
    lost_games: int = 0

    @field_validator("elo_rating", mode="before")
    @classmethod
    def round_elo(cls, v: Any) -> int:
        if isinstance(v, float):
            return int(round(v))
        return v

    class Config:
        from_attributes = True
