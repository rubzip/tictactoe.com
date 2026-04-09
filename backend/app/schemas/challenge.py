from pydantic import BaseModel
from datetime import datetime
from app.core.constants import ChallengeStatus


class ChallengeBase(BaseModel):
    challenged_id: int


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeUpdate(BaseModel):
    status: ChallengeStatus


class ChallengeInfo(ChallengeBase):
    id: int
    challenger_id: int
    room_id: str
    status: ChallengeStatus
    created_at: datetime

    class Config:
        from_attributes = True
