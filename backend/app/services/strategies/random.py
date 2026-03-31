import random

from app.core.types import BoardType
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine
from .base import Strategy


class RandomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        return random.choice(moves)
