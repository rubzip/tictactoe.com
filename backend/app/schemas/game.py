from typing import List, Annotated
from pydantic import BaseModel, Field, RootModel
from app.core.constants import GameStatus, Player, UsablePlayer


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
