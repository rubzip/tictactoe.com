from typing import List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    username: str
    message: str = Field(..., min_length=1, max_length=1000)
    room_id: str
    timestamp: float


class ChatHistory(BaseModel):
    messages: List[ChatMessage]