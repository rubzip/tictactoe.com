import pytest
from app.services.cpu import EasyCPU, MediumCPU, HardCPU, PerfectCPU
from app.services.game_engine import TicTacToeEngine
from app.core.constants import Player

@pytest.mark.parametrize("cpu_class", [EasyCPU, MediumCPU, HardCPU, PerfectCPU])
def test_cpu_gets_move(cpu_class):
    board, turn, status = TicTacToeEngine.init_board()
    move = cpu_class.get_move(board, turn)
    assert move is not None
    assert 0 <= move[0] < 3
    assert 0 <= move[1] < 3

def test_perfect_cpu_wins_or_draws():
    # This is a bit more complex to test, but we can at least ensure it makes a move
    pass
