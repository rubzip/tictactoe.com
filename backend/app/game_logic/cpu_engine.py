from typing import Type, Optional
from app.core.constants import DifficultyMode, Player
from app.core.exceptions import InvalidDifficultyException
from .game_engine import TicTacToeEngine
from .strategies import MoveType, Strategy, RandomStrategy, CustomStrategy, MinimaxStrategy


class EasyCPU(RandomStrategy):
    pass

class MediumCPU(MinimaxStrategy):
    MAX_DEPTH = 4

class HardCPU(MinimaxStrategy):
    MAX_DEPTH = 6

class PerfectCPU(MinimaxStrategy):
    MAX_DEPTH = 9


def get_strategy(difficulty: DifficultyMode) -> Type[Strategy]:
    if difficulty == DifficultyMode.EASY:
        return EasyCPU
    if difficulty == DifficultyMode.MEDIUM:
        return MediumCPU
    if difficulty == DifficultyMode.HARD:
        return HardCPU
    if difficulty == DifficultyMode.EXPERT:
        return PerfectCPU
    raise InvalidDifficultyException(str(difficulty))

def get_next_cpu_move(board, difficulty: DifficultyMode, turn: Optional[Player] = None) -> MoveType:
    """
    Returns the next move for the CPU based on difficulty.
    If turn is not provided, it will be automatically determined from the board.
    """
    strategy = get_strategy(difficulty)
    
    if turn is None:
        turn = TicTacToeEngine.get_current_player(board)
        
    return strategy.get_move(board, turn)
