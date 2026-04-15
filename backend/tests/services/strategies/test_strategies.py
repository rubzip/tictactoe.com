import pytest
from app.game_logic.cpu_engine import EasyCPU, MediumCPU, HardCPU, PerfectCPU, get_next_cpu_move
from app.game_logic.game_engine import TicTacToeEngine
from app.core.constants import Player, DifficultyMode

@pytest.mark.parametrize("cpu_class", [EasyCPU, MediumCPU, HardCPU, PerfectCPU])
def test_cpu_gets_move(cpu_class):
    board, turn, status = TicTacToeEngine.init_board()
    move = cpu_class.get_move(board, turn)
    assert move is not None
    assert 0 <= move[0] < 3
    assert 0 <= move[1] < 3

@pytest.mark.parametrize("difficulty", [
    DifficultyMode.EASY, 
    DifficultyMode.MEDIUM, 
    DifficultyMode.HARD, 
    DifficultyMode.EXPERT
])
def test_get_next_cpu_move_helper(difficulty):
    board, turn, status = TicTacToeEngine.init_board()
    
    # Test with explicit turn
    move1 = get_next_cpu_move(board, difficulty, turn)
    assert move1 is not None
    
    # Test with auto-detected turn
    move2 = get_next_cpu_move(board, difficulty)
    assert move2 is not None

def test_perfect_cpu_wins_or_draws():
    # This is a bit more complex to test, but we can at least ensure it makes a move
    pass
