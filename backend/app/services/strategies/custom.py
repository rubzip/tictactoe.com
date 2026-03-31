import random

from app.core.types import BoardType
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine

from .base import Strategy


class CustomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        for r, c in moves:
            if cls._simulate_win(board, r, c, turn):
                return (r, c)        
                
        opponent = Player.O if turn == Player.X else Player.X
        for r, c in moves:
            if cls._simulate_win(board, r, c, opponent):
                return (r, c)
                
        if (1, 1) in moves:
            return (1, 1)
            
        return random.choice(moves)

    @classmethod
    def _simulate_win(cls, board: BoardType, r: int, c: int, player: Player) -> bool:
        test_board = [row[:] for row in board]
        test_board[r][c] = player
        
        status = TicTacToeEngine.get_game_status(test_board)
        expected_status = GameStatus.WIN_X if player == Player.X else GameStatus.WIN_O
        return status == expected_status
