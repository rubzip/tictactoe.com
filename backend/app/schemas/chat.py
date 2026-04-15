from typing import List
from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    username: str
    message: str = Field(..., min_length=1, max_length=1000)
    room_id: str


class ChatMessage(ChatCreate):
    timestamp: float

    class Config:
        from_attributes = True


class ChatHistory(BaseModel):
    messages: List[ChatMessage]