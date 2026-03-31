import math
import random
from abc import ABC, abstractmethod

from app.core.types import BoardType
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine


class Strategy(ABC):
    @classmethod
    def get_move(cls, board: BoardType, turn: Player) -> tuple[int, int] | None:
        moves = TicTacToeEngine.get_possible_moves(board)
        if not moves:
            return None
        
        return cls._strategy(board, turn, moves)

    @classmethod
    @abstractmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        pass
