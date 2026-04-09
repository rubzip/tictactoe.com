import random

from app.core.constants import Player, BoardType
from .base import Strategy, MoveType


class RandomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[MoveType]) -> MoveType:
        return random.choice(moves)
