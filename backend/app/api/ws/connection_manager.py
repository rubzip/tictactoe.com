from typing import Dict, Set
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # active_connections[client_id] = WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # room_connections[room_id] = {client_id1, client_id2, ...}
        self.room_connections: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # Remove from rooms
        for room_id in list(self.room_connections.keys()):
            if client_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(client_id)
                if not self.room_connections[room_id]:
                    del self.room_connections[room_id]

    async def join_room(self, client_id: str, room_id: str):
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        self.room_connections[room_id].add(client_id)

    async def send_personal_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

    async def broadcast_to_room(self, message: dict, room_id: str):
        if room_id in self.room_connections:
            for client_id in self.room_connections[room_id]:
                if client_id in self.active_connections:
                    await self.active_connections[client_id].send_json(message)

    async def broadcast_all(self, message: dict):
        for websocket in self.active_connections.values():
            await websocket.send_json(message)


manager = ConnectionManager()
