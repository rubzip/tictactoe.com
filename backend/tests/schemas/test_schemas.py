import pytest
from app.schemas.game import GameState, Row, Board, Move
from app.schemas.user import User
from app.schemas.ws_messages import JoinMessage, MessageType
from app.core.constants import Player, GameStatus

def test_user_schema():
    user = User(id=1, username="test", email="test@example.com")
    assert user.id == 1
    assert user.elo_rating == 1000

def test_game_state_schema():
    row = Row(root=[Player.X, Player.O, Player.NONE])
    board = Board(root=[row, row, row])
    state = GameState(board=board, turn=Player.X, status=GameStatus.KEEP_PLAYING)
    assert state.turn == Player.X
    assert len(state.board.root) == 3

def test_ws_message_schema():
    msg = JoinMessage(payload={"room_id": "123"})
    assert msg.type == MessageType.JOIN
    assert msg.payload["room_id"] == "123"
