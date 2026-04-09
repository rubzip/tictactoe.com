from typing import Dict, Optional
from app.services.game_engine import TicTacToeEngine
from app.core.constants import Player, GameStatus
from app.core.types import BoardType
from dataclasses import dataclass, field


@dataclass
class GameSession:
    room_id: str
    board: BoardType = field(default_factory=lambda: TicTacToeEngine.init_board()[0])
    turn: Player = Player.X
    status: GameStatus = GameStatus.KEEP_PLAYING
    players: Dict[str, Player] = field(default_factory=dict) # client_id -> Player (X or O)


class GameService:
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}

    def get_or_create_session(self, room_id: str) -> GameSession:
        if room_id not in self.sessions:
            self.sessions[room_id] = GameSession(room_id=room_id)
        return self.sessions[room_id]

    def join_game(self, room_id: str, client_id: str) -> Optional[Player]:
        session = self.get_or_create_session(room_id)
        
        # If player already in game, return their role
        if client_id in session.players:
            return session.players[client_id]
        
        # Assign role if possible
        if len(session.players) == 0:
            session.players[client_id] = Player.X
            return Player.X
        elif len(session.players) == 1:
            session.players[client_id] = Player.O
            return Player.O
        
        # Room full (as a player, could be spectator)
        return None

    def make_move(self, room_id: str, client_id: str, row: int, col: int) -> dict:
        session = self.sessions.get(room_id)
        if not session:
            return {"error": "Game not found"}
            
        player = session.players.get(client_id)
        if not player:
            return {"error": "Player not in this game"}

        try:
            new_board, next_turn, new_status = TicTacToeEngine.make_move(
                session.board, session.turn, player, row, col
            )
            session.board = new_board
            session.turn = next_turn
            session.status = new_status
            
            return {
                "board": session.board,
                "turn": session.turn,
                "status": session.status,
                "player": player,
                "row": row,
                "col": col
            }
        except Exception as e:
            return {"error": str(e)}


game_service = GameService()
