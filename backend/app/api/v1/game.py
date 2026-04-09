from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.game import Move, GameState
from app.services.game_service import game_service
from app.core.constants import DifficultyMode, Player
from app.api import deps
from app.models.users import User
import uuid

router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@router.post("/ai/start", response_model=dict)
def start_ai_game(
    difficulty: DifficultyMode,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Start a new game against the CPU.
    """
    room_id = f"ai_{uuid.uuid4()}"
    session = game_service.get_or_create_session(
        db,
        room_id, 
        is_ai=True, 
        difficulty=difficulty
    )
    
    # Auto-join the player with their user_id for stat tracking
    game_service.join_game(db, room_id, client_id=current_user.username, user_id=current_user.id)
    
    return {
        "room_id": room_id,
        "difficulty": difficulty,
        "player_role": Player.X,
        "status": session.status,
        "board": session.board
    }


@router.post("/move", response_model=dict)
def make_move(
    room_id: str,
    move: Move,
    client_id: str = "guest",
    db: Session = Depends(deps.get_db)
):
    """
    Make a move in a game session.
    """
    result = game_service.make_move(
        db,
        room_id, 
        client_id, 
        move.row, 
        move.col
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
        
    return result
