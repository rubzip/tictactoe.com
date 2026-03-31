from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    MOVE = "MOVE"
    GAME_STATE = "GAME_STATE"
    CHAT = "CHAT"
    ERROR = "ERROR"
    JOIN = "JOIN"
    LEAVE = "LEAVE"


class BaseWSMessage(BaseModel):
    type: MessageType
    payload: Any


class JoinMessage(BaseWSMessage):
    type: Literal[MessageType.JOIN] = MessageType.JOIN
    payload: dict[str, str]  # e.g. {"room_id": "game1"}


class MoveMessage(BaseWSMessage):
    type: Literal[MessageType.MOVE] = MessageType.MOVE
    payload: dict[str, int]  # e.g. {"row": 0, "col": 1}


class ChatMessage(BaseWSMessage):
    type: Literal[MessageType.CHAT] = MessageType.CHAT
    payload: str


class ErrorMessage(BaseWSMessage):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    payload: str
