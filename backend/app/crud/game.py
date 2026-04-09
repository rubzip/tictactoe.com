from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.models.game import Game
from app.core.constants import Player, GameStatus, DifficultyMode


def get_game_by_room(db: Session, room_id: str) -> Game | None:
    return db.query(Game).filter(Game.room_id == room_id).first()


def create_game(
    db: Session, 
    room_id: str, 
    board: list[list[str]], 
    is_ai: bool = False, 
    difficulty: DifficultyMode = None
) -> Game:
    db_game = Game(
        room_id=room_id,
        board=board,
        turn=Player.X,
        status=GameStatus.KEEP_PLAYING,
        is_ai_game=is_ai,
        ai_difficulty=difficulty
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(
    db: Session, 
    room_id: str, 
    board: list[list[str]], 
    turn: Player, 
    status: GameStatus, 
    win_line: list = None
) -> Game | None:
    db_game = get_game_by_room(db, room_id)
    if not db_game:
        return None
    
    db_game.board = board
    db_game.turn = turn
    db_game.status = status
    if win_line is not None:
        db_game.win_line = win_line
        flag_modified(db_game, "win_line")
        
    # Force SQLAlchemy to see the change in board
    flag_modified(db_game, "board")
        
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
