from typing import List, Annotated
from pydantic import BaseModel, Field, RootModel
from app.core.constants import GameStatus, Player
from app.core.types import UsablePlayer, Board


class Move(BaseModel):
    row: Annotated[int, Field(ge=0, le=2)]
    col: Annotated[int, Field(ge=0, le=2)]

class History(BaseModel):
    pass

class Row(BaseModel):
    root: List[Player] = Field(..., min_length=3, max_length=3)

class Board(BaseModel):
    board: List[Row] = Field(..., min_length=3, max_length=3)

class GameState(BaseModel):
    board: List[Row] = Field(..., min_length=3, max_length=3)
    turn: Player
    status: GameStatus
