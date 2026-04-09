from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from app.services.game_engine import TicTacToeEngine
from app.services.cpu import get_next_cpu_move
from app.core.constants import Player, GameStatus, DifficultyMode, BoardType
from dataclasses import dataclass, field
import app.crud.game as crud_game


@dataclass
class GameSession:
    room_id: str
    board: BoardType
    turn: Player
    status: GameStatus
    win_line: List[tuple[int, int]] = field(default_factory=list)
    players: Dict[str, Player] = field(default_factory=dict) # client_id -> Player (X or O)
    
    # AI Game specific fields
    is_ai_game: bool = False
    ai_difficulty: Optional[DifficultyMode] = None
    ai_player: Player = Player.O


class GameService:
    def __init__(self):
        # We still keep in-memory sessions for tracking connected players
        self.sessions: Dict[str, GameSession] = {}

    def _sync_with_db(self, db: Session, room_id: str, is_ai: bool = False, difficulty: DifficultyMode = None) -> GameSession:
        """Fetch from DB and sync with in-memory session."""
        db_game = crud_game.get_game_by_room(db, room_id)
        if not db_game:
            # Create new game in DB if doesn't exist
            initial_board, _, _ = TicTacToeEngine.init_board()
            db_game = crud_game.create_game(
                db, 
                room_id=room_id, 
                board=initial_board, 
                is_ai=is_ai, 
                difficulty=difficulty
            )
        
        # Load into memory if not there, or update from DB
        if room_id not in self.sessions:
            self.sessions[room_id] = GameSession(
                room_id=room_id,
                board=db_game.board,
                turn=db_game.turn,
                status=db_game.status,
                win_line=db_game.win_line if db_game.win_line else [],
                is_ai_game=db_game.is_ai_game,
                ai_difficulty=db_game.ai_difficulty,
                ai_player=db_game.ai_player
            )
        else:
            # Sync existing session with DB state (in case of REST updates)
            session = self.sessions[room_id]
            session.board = db_game.board
            session.turn = db_game.turn
            session.status = db_game.status
            session.win_line = db_game.win_line if db_game.win_line else []
            
        return self.sessions[room_id]

    def get_or_create_session(self, db: Session, room_id: str, is_ai: bool = False, difficulty: DifficultyMode = None) -> GameSession:
        return self._sync_with_db(db, room_id, is_ai, difficulty)

    def join_game(self, db: Session, room_id: str, client_id: str) -> Optional[Player]:
        session = self.get_or_create_session(db, room_id)
        
        # If player already in game, return their role
        if client_id in session.players:
            return session.players[client_id]
        
        # Assign role if possible
        if len(session.players) == 0:
            session.players[client_id] = Player.X
            return Player.X
        elif len(session.players) == 1 and not session.is_ai_game:
            session.players[client_id] = Player.O
            return Player.O
        
        # Room full or already has AI
        return None

    def make_move(self, db: Session, room_id: str, client_id: str, row: int, col: int) -> dict:
        # Ensure session is in sync with DB
        db_game = crud_game.get_game_by_room(db, room_id)
        if not db_game:
            return {"error": "Game not found"}
            
        session = self._sync_with_db(db, room_id)
        
        player = session.players.get(client_id)
        if not player:
            return {"error": "Player not in this game"}

        try:
            # 1. Human Move
            session.board, session.turn, session.status, session.win_line = TicTacToeEngine.make_move(
                session.board, session.turn, player, row, col
            )
            
            # Update DB with Human Move
            crud_game.update_game(
                db, 
                room_id=room_id, 
                board=session.board, 
                turn=session.turn, 
                status=session.status, 
                win_line=session.win_line
            )
            
            result = {
                "board": session.board,
                "turn": session.turn,
                "status": session.status,
                "win_line": session.win_line,
                "player": player,
                "row": row,
                "col": col
            }

            # 2. Trigger CPU Move if applicable
            if (session.is_ai_game and 
                session.status == GameStatus.KEEP_PLAYING and 
                session.turn == session.ai_player):
                
                cpu_row, cpu_col = get_next_cpu_move(
                    session.board, 
                    session.ai_difficulty, 
                    session.ai_player
                )
                
                session.board, session.turn, session.status, session.win_line = TicTacToeEngine.make_move(
                    session.board, session.turn, session.ai_player, cpu_row, cpu_col
                )
                
                # Update DB with CPU Move
                crud_game.update_game(
                    db, 
                    room_id=room_id, 
                    board=session.board, 
                    turn=session.turn, 
                    status=session.status, 
                    win_line=session.win_line
                )
                
                result["cpu_move"] = {
                    "row": cpu_row,
                    "col": cpu_col,
                    "player": session.ai_player,
                    "board": session.board,
                    "turn": session.turn,
                    "status": session.status,
                    "win_line": session.win_line
                }
                
                # Update the main result with the absolute final state
                result["board"] = session.board
                result["turn"] = session.turn
                result["status"] = session.status
            
            return result
            
        except Exception as e:
            return {"error": str(e)}


game_service = GameService()
