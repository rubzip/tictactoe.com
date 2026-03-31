import math
import random
from abc import ABC, abstractmethod

from app.core.types import Board
from app.core.constants import GameStatus, Player
from app.services.game_engine import TicTacToeEngine


class Strategy(ABC):
    @classmethod
    def get_move(cls, board: Board, turn: Player) -> tuple[int, int] | None:
        moves = cls.get_possible_moves(board)
        if not moves:
            return None
        
        return cls._strategy(board, turn, moves)

    @classmethod
    @abstractmethod
    def _strategy(cls, board: Board, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        pass

    @staticmethod
    def get_possible_moves(board: Board) -> list[tuple[int, int]]:
        status = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return []
            
        moves = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == Player.NONE:
                    moves.append((r, c))
        return moves


class RandomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: Board, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
        return random.choice(moves)


class CustomStrategy(Strategy):
    @classmethod
    def _strategy(cls, board: Board, turn: Player, moves: list[tuple[int, int]]) -> tuple[int, int]:
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
    def _simulate_win(cls, board: Board, r: int, c: int, player: Player) -> bool:
        test_board = [row[:] for row in board]
        test_board[r][c] = player
        
        status = TicTacToeEngine.get_game_status(test_board)
        expected_status = GameStatus.WIN_X if player == Player.X else GameStatus.WIN_O
        return status == expected_status


class MinimaxStrategy(Strategy):
    MAX_DEPTH = 3
    @classmethod
    def _strategy(cls, board: Board, turn: Player, moves: list[tuple[int, int]], max_depth: int) -> tuple[int, int]:
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
    def _minimax(cls, board: Board, is_maximizing: bool, bot_player: Player, depth: int) -> float:
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

        moves = cls.get_possible_moves(board)
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








