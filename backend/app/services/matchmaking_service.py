import asyncio
import uuid
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

from app.core.constants import Player, GameStatus
from app.api.ws.connection_manager import manager
from app.schemas.ws_messages import MessageType


@dataclass
class QueuedPlayer:
    username: str
    client_id: str
    elo: int
    joined_at: datetime = field(default_factory=datetime.now)
    wait_time_seconds: int = 0


class MatchmakingService:
    def __init__(self):
        # queue[username] = QueuedPlayer
        self.queue: Dict[str, QueuedPlayer] = {}
        self.is_running = False
        self._lock = asyncio.Lock()

    async def add_to_queue(self, username: str, client_id: str, elo: int):
        async with self._lock:
            if username in self.queue:
                return # Already in queue
            
            self.queue[username] = QueuedPlayer(
                username=username,
                client_id=client_id,
                elo=elo
            )
            print(f"Player {username} joined matchmaking queue (Elo: {elo})")

    async def remove_from_queue(self, username: str):
        async with self._lock:
            if username in self.queue:
                del self.queue[username]
                print(f"Player {username} left matchmaking queue")

    async def run_matchmaker(self):
        """Background task to match players."""
        self.is_running = True
        while self.is_running:
            await self._find_matches()
            await asyncio.sleep(2) # Run every 2 seconds

    async def _find_matches(self):
        async with self._lock:
            if len(self.queue) < 2:
                return

            # Simple matchmaking: Sort by Elo and match adjacent players if they are within range
            # Range increases with wait time
            sorted_players = sorted(
                self.queue.values(), 
                key=lambda p: (p.elo, p.joined_at)
            )

            matched_usernames = set()
            
            for i in range(len(sorted_players) - 1):
                p1 = sorted_players[i]
                p2 = sorted_players[i+1]

                if p1.username in matched_usernames or p2.username in matched_usernames:
                    continue

                # Wait time in seconds
                p1.wait_time_seconds = (datetime.now() - p1.joined_at).total_seconds()
                p2.wait_time_seconds = (datetime.now() - p2.joined_at).total_seconds()

                # Basic Elo range: starts at 100, increases by 50 every 10 seconds of wait
                allowed_range = 100 + (min(p1.wait_time_seconds, p2.wait_time_seconds) // 10) * 50
                
                elo_diff = abs(p1.elo - p2.elo)
                
                if elo_diff <= allowed_range:
                    # Match found!
                    matched_usernames.add(p1.username)
                    matched_usernames.add(p2.username)
                    await self._create_match(p1, p2)

            # Remove matched players from queue
            for username in matched_usernames:
                if username in self.queue:
                    del self.queue[username]

    async def _create_match(self, p1: QueuedPlayer, p2: QueuedPlayer):
        room_id = f"match_{uuid.uuid4().hex[:8]}"
        print(f"Match found! {p1.username} vs {p2.username} in room {room_id}")

        # Notify players
        # Player 1 (X)
        await manager.send_personal_message({
            "type": MessageType.MATCH_FOUND,
            "payload": {
                "room_id": room_id,
                "opponent": p2.username,
                "role": Player.X
            }
        }, p1.client_id)

        # Player 2 (O)
        await manager.send_personal_message({
            "type": MessageType.MATCH_FOUND,
            "payload": {
                "room_id": room_id,
                "opponent": p1.username,
                "role": Player.O
            }
        }, p2.client_id)


matchmaking_service = MatchmakingService()
