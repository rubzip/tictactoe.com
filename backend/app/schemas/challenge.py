from pydantic import BaseModel
from datetime import datetime
from app.core.constants import ChallengeStatus


class ChallengeBase(BaseModel):
    challenged_username: str


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeUpdate(BaseModel):
    status: ChallengeStatus


class ChallengeInfo(ChallengeBase):
    id: int
    challenger_username: str
    room_id: str
    status: ChallengeStatus
    created_at: datetime

    class Config:
        from_attributes = True
