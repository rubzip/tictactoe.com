import math
import random
from abc import ABC, abstractmethod

from app.core.types import BoardType
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine


class Strategy(ABC):
    @classmethod
    def get_move(cls, board: BoardType, turn: Player) -> tuple[int, int] | None:
        moves = cls.get_possible_moves(board)
        if not moves:
            return None
        
        return cls._strategy(board, turn, moves)

    @classmethod
    @abstractmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        pass

    @staticmethod
    def get_possible_moves(board: BoardType) -> list[tuple[int, int]]:
        status = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return []
            
        moves = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == Player.NONE:
                    moves.append((r, c))
        return moves
