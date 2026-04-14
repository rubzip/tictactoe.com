from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.models.game import Game
from app.core.constants import Player, GameStatus, DifficultyMode
from app.game_logic.game_engine import TicTacToeEngine

from app.schemas.game import GameCreate, GameUpdate


def get_game_by_room(db: Session, room_id: str) -> Game | None:
    return db.query(Game).filter(Game.room_id == room_id).first()


def create_game(db: Session, game_in: GameCreate) -> Game:
    # Initialize empty board if not provided (though models usually handle this)
    board, turn, status = TicTacToeEngine.init_board()
    
    db_game = Game(
        room_id=game_in.room_id,
        board=board,
        turn=turn,
        status=status,
        player_x_username=game_in.player_x_username,
        player_o_username=game_in.player_o_username,
        ai_player_x_difficulty=game_in.ai_player_x_difficulty,
        ai_player_o_difficulty=game_in.ai_player_o_difficulty
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(db: Session, room_id: str, game_in: GameUpdate) -> Game | None:
    db_game = get_game_by_room(db, room_id)
    if not db_game:
        return None
    
    update_data = game_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_game, field, value)
        if field in ["board", "win_line"]:
            flag_modified(db_game, field)
        
    db.commit()
    db.refresh(db_game)
    return db_game


def delete_game(db: Session, room_id: str) -> bool:
    db_game = get_game_by_room(db, room_id)
    if db_game:
        db.delete(db_game)
        db.commit()
        return True
    return False


def get_user_match_history(db: Session, username: str, limit: int = 20) -> list[Game]:
    return db.query(Game).filter(
        (Game.player_x_username == username) | (Game.player_o_username == username)
    ).order_by(Game.created_at.desc()).limit(limit).all()
