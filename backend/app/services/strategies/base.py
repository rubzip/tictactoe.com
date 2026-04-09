from abc import ABC, abstractmethod

from app.core.types import BoardType
from app.core.constants import Player
from app.services.game_engine import TicTacToeEngine

MoveType = tuple[int, int]

class Strategy(ABC):
    @classmethod
    def get_move(cls, board: BoardType, turn: Player) -> MoveType | None:
        moves = TicTacToeEngine.get_possible_moves(board)
        if not moves:
            return None
        
        return cls._strategy(board, turn, moves)

    @classmethod
    @abstractmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[MoveType]) -> MoveType:
        pass
