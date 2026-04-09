import math

from app.core.types import BoardType
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine
from .base import Strategy


class MinimaxStrategy(Strategy):
    MAX_DEPTH = 3
    @classmethod
    def _strategy(cls, board: BoardType, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        best_score = -math.inf
        best_move = moves[0]

        for r, c in moves:
            test_board = [row[:] for row in board]
            test_board[r][c] = turn
            
            score = cls._minimax(test_board, is_maximizing=False, bot_player=turn, depth=cls.MAX_DEPTH - 1)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    @classmethod
    def _minimax(cls, board: BoardType, is_maximizing: bool, bot_player: Player, depth: int) -> float:
        status = TicTacToeEngine.get_game_status(board)

        bot_win = GameStatus.WIN_X if bot_player == Player.X else GameStatus.WIN_O
        human_win = GameStatus.WIN_O if bot_player == Player.X else GameStatus.WIN_X

        if status == bot_win:
            return 10 + depth
        elif status == human_win:
            return -10 - depth
        elif status == GameStatus.DRAW:
            return 0

        if depth == 0:
            return 0

        moves = TicTacToeEngine.get_possible_moves(board)
        current_turn = bot_player if is_maximizing else (Player.O if bot_player == Player.X else Player.X)

        if is_maximizing:
            best_score = -math.inf
            for r, c in moves:
                test_board = [row[:] for row in board]
                test_board[r][c] = current_turn
                score = cls._minimax(test_board, False, bot_player, depth - 1)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r, c in moves:
                test_board = [row[:] for row in board]
                test_board[r][c] = current_turn
                score = cls._minimax(test_board, True, bot_player, depth - 1)
                best_score = min(score, best_score)
            return best_score
