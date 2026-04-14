import pytest
from app.core.constants import Player, GameStatus
from app.game_logic.game_engine import TicTacToeEngine
from app.core.exceptions import InvalidMoveException, OccupiedCellException, GameOverException

def test_init_board():
    board, turn, status = TicTacToeEngine.init_board()
    assert len(board) == 3
    assert all(len(row) == 3 for row in board)
    assert all(cell == Player.NONE for row in board for cell in row)
    assert turn == Player.X
    assert status == GameStatus.KEEP_PLAYING

def test_get_game_status_win_x():
    board = [
        [Player.X, Player.X, Player.X],
        [Player.O, Player.O, Player.NONE],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    status, win_line = TicTacToeEngine.get_game_status(board)
    assert status == GameStatus.WIN_X
    assert win_line == [(0, 0), (0, 1), (0, 2)]

def test_get_game_status_win_o():
    board = [
        [Player.X, Player.X, Player.NONE],
        [Player.O, Player.O, Player.O],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    status, win_line = TicTacToeEngine.get_game_status(board)
    assert status == GameStatus.WIN_O
    assert win_line == [(1, 0), (1, 1), (1, 2)]

def test_get_game_status_draw():
    board = [
        [Player.X, Player.O, Player.X],
        [Player.X, Player.O, Player.O],
        [Player.O, Player.X, Player.X]
    ]
    status, win_line = TicTacToeEngine.get_game_status(board)
    assert status == GameStatus.DRAW
    assert win_line == []

def test_make_move():
    board, turn, status = TicTacToeEngine.init_board()
    new_board, next_turn, next_status, win_line = TicTacToeEngine.make_move(board, turn, Player.X, 0, 0)
    assert new_board[0][0] == Player.X
    assert next_turn == Player.O
    assert next_status == GameStatus.KEEP_PLAYING

def test_make_move_invalid_player():
    board, turn, status = TicTacToeEngine.init_board()
    with pytest.raises(InvalidMoveException, match="Now is X turn"):
        TicTacToeEngine.make_move(board, turn, Player.O, 0, 0)

def test_make_move_occupied_cell():
    board = [[Player.X, Player.NONE, Player.NONE], [Player.NONE]*3, [Player.NONE]*3]
    turn = Player.O
    with pytest.raises(OccupiedCellException, match="already occupied"):
        TicTacToeEngine.make_move(board, turn, Player.O, 0, 0)
