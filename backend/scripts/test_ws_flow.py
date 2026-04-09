import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/test_client"
    async with websockets.connect(uri) as websocket:
        # Join room
        join_msg = {
            "type": "JOIN",
            "payload": {"room_id": "game1"}
        }
        await websocket.send(json.dumps(join_msg))
        
        # Receive JOIN response and INITIAL GAME_STATE
        for _ in range(2):
            resp = await websocket.recv()
            print(f"Received: {resp}")
            
        # Make a move
        move_msg = {
            "type": "MOVE",
            "payload": {"room_id": "game1", "row": 0, "col": 0}
        }
        await websocket.send(json.dumps(move_msg))
        
        # Receive MOVE response (GAME_STATE)
        resp = await websocket.recv()
        print(f"Received: {resp}")

if __name__ == "__main__":
    asyncio.run(test_ws())
