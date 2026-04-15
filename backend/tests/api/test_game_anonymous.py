import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.constants import DifficultyMode

client = TestClient(app)

def test_start_ai_game_anonymous():
    """Test starting an AI game without authentication."""
    response = client.post(
        "/api/v1/game/ai/start",
        params={"difficulty": DifficultyMode.EASY.value, "client_id": "test_guest_123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "room_id" in data
    assert data["ai_player_o_difficulty"] == DifficultyMode.EASY.value
    # Anonymous games shouldn't have associated usernames in DB initially if not provided
    assert data["player_x_username"] is None
    assert data["player_o_username"] is None

def test_make_move_anonymous():
    """Test making a move in an AI game without authentication."""
    # 1. Start game
    start_resp = client.post(
        "/api/v1/game/ai/start",
        params={"difficulty": DifficultyMode.EASY.value, "client_id": "test_guest_move"}
    )
    room_id = start_resp.json()["room_id"]
    
    # 2. Make move
    move_resp = client.post(
        "/api/v1/game/move",
        params={"room_id": room_id, "client_id": "test_guest_move"},
        json={"row": 0, "col": 0, "player": "X"}
    )
    assert move_resp.status_code == 200
    move_data = move_resp.json()
    assert move_data["board"][0][0] == "X"
    # CPU should have moved
    cpu_moves = move_data.get("cpu_moves", [])
    assert len(cpu_moves) > 0

def test_websocket_anonymous_join():
    """Test connecting to WebSocket and joining room without authentication."""
    # 1. Start game via REST
    start_resp = client.post(
        "/api/v1/game/ai/start",
        params={"difficulty": DifficultyMode.EASY.value, "client_id": "ws_guest"}
    )
    room_id = start_resp.json()["room_id"]
    
    # 2. Connect via WS
    with client.websocket_connect("/ws/ws_guest") as websocket:
        # Join room
        websocket.send_json({
            "type": "JOIN",
            "payload": {"room_id": room_id}
        })
        
        # Should receive JOIN success
        response = websocket.receive_json()
        assert response["type"] == "JOIN"
        assert response["payload"]["status"] == "success"
        assert response["payload"]["room_id"] == room_id

def test_matchmaking_anonymous_denied():
    """Test that anonymous users cannot join matchmaking."""
    with client.websocket_connect("/ws/anon_match") as websocket:
        websocket.send_json({
            "type": "QUEUE_JOIN",
            "payload": {}
        })
        
        response = websocket.receive_json()
        assert response["type"] == "ERROR"
        assert "Authentication required" in response["payload"]
