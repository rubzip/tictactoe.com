from typing import List, Annotated, Optional
from pydantic import BaseModel, Field, RootModel, ConfigDict
from datetime import datetime
from app.core.constants import GameStatus, Player, UsablePlayer, DifficultyMode


class Move(BaseModel):
    row: Annotated[int, Field(ge=0, le=2)]
    col: Annotated[int, Field(ge=0, le=2)]
    player: UsablePlayer


class History(BaseModel):
    moves: List[Move] = Field(default_factory=list)


class Row(RootModel):
    root: List[Player] = Field(..., min_length=3, max_length=3)


class Board(RootModel):
    root: List[Row] = Field(..., min_length=3, max_length=3)


class GameState(BaseModel):
    board: Board
    turn: Player
    status: GameStatus
    win_line: Optional[List[List[int]]] = None


class GameCreate(BaseModel):
    room_id: str
    player_x_username: Optional[str] = None
    player_o_username: Optional[str] = None
    ai_player_x_difficulty: Optional[DifficultyMode] = None
    ai_player_o_difficulty: Optional[DifficultyMode] = None


class GameUpdate(BaseModel):
    board: Optional[Board] = None
    turn: Optional[Player] = None
    status: Optional[GameStatus] = None
    win_line: Optional[List[List[int]]] = None
    player_x_username: Optional[str] = None
    player_o_username: Optional[str] = None


class GameInfo(GameState):
    model_config = ConfigDict(from_attributes=True)

    room_id: str
    player_x_username: Optional[str] = None
    player_o_username: Optional[str] = None
    ai_player_x_difficulty: Optional[DifficultyMode] = None
    ai_player_o_difficulty: Optional[DifficultyMode] = None
    created_at: Optional[datetime] = None


class MatchHistory(BaseModel):
    matches: List[GameInfo]
