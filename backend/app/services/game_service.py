from typing import Dict, Optional, List, Set
from sqlalchemy.orm import Session
from app.game_logic.game_engine import TicTacToeEngine
from app.game_logic.cpu_engine import get_next_cpu_move
from app.core.constants import Player, GameStatus, DifficultyMode, BoardType
from dataclasses import dataclass, field
import app.crud.game as crud_game
from app.schemas.game import GameCreate, GameUpdate
from app.core.exceptions import BaseAppException, RoomNotFoundException, InvalidMoveException


@dataclass
class GameSession:
    room_id: str
    board: BoardType
    turn: Player
    status: GameStatus
    win_line: List[tuple[int, int]] = field(default_factory=list)
    players: Dict[str, Player] = field(default_factory=dict) # client_id -> Player (X or O)
    spectators: Set[str] = field(default_factory=set) # Set of client_ids
    player_usernames: Dict[Player, str] = field(default_factory=dict) # Player -> username
    
    # AI Game specific fields
    ai_player_x_difficulty: Optional[DifficultyMode] = field(default=None)
    ai_player_o_difficulty: Optional[DifficultyMode] = field(default=None)

    @property
    def is_ai_game(self) -> bool:
        return self.ai_player_x_difficulty is not None or self.ai_player_o_difficulty is not None

    def to_summary_dict(self) -> dict:
        """Returns a dict suitable for WebSocket/API responses."""
        return {
            "board": self.board,
            "turn": self.turn,
            "status": self.status,
            "win_line": self.win_line,
            "player_usernames": {k.value: v for k, v in self.player_usernames.items()},
            "ai_difficulties": {
                "X": self.ai_player_x_difficulty,
                "O": self.ai_player_o_difficulty
            }
        }


class GameService:
    def __init__(self):
        # We still keep in-memory sessions for tracking connected players
        self.sessions: Dict[str, GameSession] = {}

    def _sync_with_db(self, db: Session, room_id: str, ai_difficulty: DifficultyMode = None, create_if_missing: bool = False) -> GameSession:
        """Fetch from DB and sync with in-memory session."""
        db_game = crud_game.get_game_by_room(db, room_id)
        if not db_game:
            if not create_if_missing:
                raise RoomNotFoundException(room_id)
            # Create new game in DB if doesn't exist
            db_game = crud_game.create_game(
                db, 
                game_in=GameCreate(
                    room_id=room_id,
                    ai_player_o_difficulty=ai_difficulty
                )
            )
        
        # Load into memory if not there, or update from DB
        if room_id not in self.sessions:
            self.sessions[room_id] = GameSession(
                room_id=room_id,
                board=db_game.board,
                turn=db_game.turn,
                status=db_game.status,
                win_line=db_game.win_line if db_game.win_line else [],
                ai_player_x_difficulty=db_game.ai_player_x_difficulty,
                ai_player_o_difficulty=db_game.ai_player_o_difficulty
            )
            # Restore players if stored in DB (partially for now)
            if db_game.player_x_username:
                self.sessions[room_id].player_usernames[Player.X] = db_game.player_x_username
            if db_game.player_o_username:
                self.sessions[room_id].player_usernames[Player.O] = db_game.player_o_username
        else:
            # Sync existing session with DB state (in case of REST updates)
            session = self.sessions[room_id]
            session.board = db_game.board
            session.turn = db_game.turn
            session.status = db_game.status
            session.win_line = db_game.win_line if db_game.win_line else []
            
        return self.sessions[room_id]

    def get_session(self, db: Session, room_id: str) -> GameSession:
        return self._sync_with_db(db, room_id, create_if_missing=False)

    def get_or_create_session(self, db: Session, room_id: str, ai_difficulty: DifficultyMode = None) -> GameSession:
        return self._sync_with_db(db, room_id, ai_difficulty=ai_difficulty, create_if_missing=True)

    def join_game(self, db: Session, room_id: str, client_id: str, username: str = None, as_spectator: bool = False) -> Optional[Player]:
        session = self.get_session(db, room_id)
        
        if as_spectator:
            session.spectators.add(client_id)
            return None # Spectators don't have a Player role (X/O)

        # If player already in game (by client_id), return their role
        if client_id in session.players:
            return session.players[client_id]
        
        # If player already in game (by username), re-associate the new client_id
        if username:
            for role, u in session.player_usernames.items():
                if u == username:
                    session.players[client_id] = role
                    return role
        
        # Assign role if possible (X then O)
        role = None
        if len(session.player_usernames) == 0:
            role = Player.X
        elif len(session.player_usernames) == 1 and not session.is_ai_game:
            # Avoid assignment if the same user tries to join twice? 
            # (Though player_usernames check above would catch it)
            if Player.X not in session.player_usernames:
                role = Player.X
            else:
                role = Player.O
        
        if role:
            session.players[client_id] = role
            if username:
                session.player_usernames[role] = username
                # Persist to DB if it's the first time
                self._update_db_players(db, room_id, session)
            return role
            
        # Room full or already has AI -> Join as spectator automatically if not rejected
        session.spectators.add(client_id)
        return None

    def make_move(self, db: Session, room_id: str, client_id: str, row: int, col: int) -> dict:
        from app.services.rating_service import rating_service
        from app.crud.user import get_user
        
        # Ensure session is in sync with DB - done once
        session = self._sync_with_db(db, room_id)
        
        player = session.players.get(client_id)
        if not player:
            return {"error": "Player not in this game"}

        try:
            # 1. Human Move
            session.board, session.turn, session.status, session.win_line = TicTacToeEngine.make_move(
                session.board, session.turn, player, row, col
            )
            self._update_db_state(db, room_id, session)
            
            result = session.to_summary_dict()
            result.update({"player": player, "row": row, "col": col})

            # 2. Trigger CPU Move if applicable
            while session.status == GameStatus.KEEP_PLAYING:
                current_ai_difficulty = session.ai_player_x_difficulty if session.turn == Player.X else session.ai_player_o_difficulty
                
                if not current_ai_difficulty:
                    break
                    
                cpu_row, cpu_col = get_next_cpu_move(session.board, current_ai_difficulty, session.turn)
                cpu_player = session.turn
                
                session.board, session.turn, session.status, session.win_line = TicTacToeEngine.make_move(
                    session.board, session.turn, cpu_player, cpu_row, cpu_col
                )
                self._update_db_state(db, room_id, session)
                
                if "cpu_moves" not in result:
                    result["cpu_moves"] = []
                
                result["cpu_moves"].append({
                    "row": cpu_row,
                    "col": cpu_col,
                    "player": cpu_player,
                    **session.to_summary_dict()
                })
            
            # Update the main result with the absolute final state
            result.update(session.to_summary_dict())

            # 3. Handle Game End - Update Stats
            if session.status != GameStatus.KEEP_PLAYING:
                self._handle_game_end(db, session)
                self.cleanup_old_sessions()
            
            return result
            
        except BaseAppException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise BaseAppException(f"Internal game error: {str(e)}")

    def _update_db_state(self, db: Session, room_id: str, session: GameSession):
        """Helper to sync current session state to DB."""
        crud_game.update_game(
            db, 
            room_id=room_id, 
            game_in=GameUpdate(
                board=session.board,
                turn=session.turn,
                status=session.status,
                win_line=session.win_line
            )
        )

    def _update_db_players(self, db: Session, room_id: str, session: GameSession):
        """Helper to sync player usernames to DB."""
        crud_game.update_game(
            db,
            room_id=room_id,
            game_in=GameUpdate(
                player_x_username=session.player_usernames.get(Player.X),
                player_o_username=session.player_usernames.get(Player.O)
            )
        )

    def _handle_game_end(self, db: Session, session: GameSession):
        from app.services.rating_service import rating_service
        
        # We only update if it's a valid end result (WIN_X, WIN_O, DRAW)
        if session.status in [GameStatus.WIN_X, GameStatus.WIN_O, GameStatus.DRAW]:
            rating_service.update_user_game_stats(
                db, 
                username_x=session.player_usernames.get(Player.X),
                username_o=session.player_usernames.get(Player.O),
                game_result=session.status
            )

    def cleanup_old_sessions(self):
        """Removes sessions for games that are finished or inactive."""
        # This could be called periodically or on certain events
        rooms_to_delete = []
        for room_id, session in self.sessions.items():
            if session.status != GameStatus.KEEP_PLAYING:
                rooms_to_delete.append(room_id)
        
        for room_id in rooms_to_delete:
            del self.sessions[room_id]


game_service = GameService()
