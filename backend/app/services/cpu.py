from app.core.constants import DifficultyMode
from app.services.strategies import RandomStrategy, CustomStrategy, MinimaxStrategy


class EasyCPU(RandomStrategy):
    pass

class MediumCPU(MinimaxStrategy):
    MAX_DEPTH = 2

class HardCPU(CustomStrategy):
    pass

class PerfectCPU(MinimaxStrategy):
    MAX_DEPTH = 9


def get_strategy(difficulty: DifficultyMode):
    if difficulty == DifficultyMode.EASY:
        return EasyCPU
    if difficulty == DifficultyMode.MEDIUM:
        return MediumCPU
    if difficulty == DifficultyMode.HARD:
        return HardCPU
    if difficulty == DifficultyMode.EXPERT:
        return PerfectCPU
    raise

def get_next_cpu_move(board, difficulty: DifficultyMode):
    strategy = get_strategy(difficulty)
    return strategy.get_move(board)
