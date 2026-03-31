import pytest
from app.core.constants import Player, GameStatus
from app.services.game_engine import TicTacToeEngine

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
    assert TicTacToeEngine.get_game_status(board) == GameStatus.WIN_X

def test_get_game_status_win_o():
    board = [
        [Player.X, Player.X, Player.NONE],
        [Player.O, Player.O, Player.O],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    assert TicTacToeEngine.get_game_status(board) == GameStatus.WIN_O

def test_get_game_status_draw():
    board = [
        [Player.X, Player.O, Player.X],
        [Player.X, Player.O, Player.O],
        [Player.O, Player.X, Player.X]
    ]
    assert TicTacToeEngine.get_game_status(board) == GameStatus.DRAW

def test_make_move():
    board, turn, status = TicTacToeEngine.init_board()
    new_board, next_turn, next_status = TicTacToeEngine.make_move(board, turn, Player.X, 0, 0)
    assert new_board[0][0] == Player.X
    assert next_turn == Player.O
    assert next_status == GameStatus.KEEP_PLAYING

def test_make_move_invalid_player():
    board, turn, status = TicTacToeEngine.init_board()
    with pytest.raises(ValueError, match="Now is X turn"):
        TicTacToeEngine.make_move(board, turn, Player.O, 0, 0)

def test_make_move_occupied_cell():
    board = [[Player.X, Player.NONE, Player.NONE], [Player.NONE]*3, [Player.NONE]*3]
    turn = Player.O
    with pytest.raises(ValueError, match="Occupied cell"):
        TicTacToeEngine.make_move(board, turn, Player.O, 0, 0)
