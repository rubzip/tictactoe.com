import random

from app.core.types import BoardType
from app.core.constants import Player
from .base import Strategy


class RandomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        return random.choice(moves)
