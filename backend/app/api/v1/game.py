from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.game_service import game_service
from app.core.constants import DifficultyMode, Player
from app.api import deps
from app.schemas.game import Move, GameState, GameInfo
from app.schemas.chat import ChatHistory, ChatMessage
from app import crud
from app.models.users import User
import uuid

router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@router.post("/ai/start", response_model=GameInfo)
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
        ai_difficulty=difficulty
    )
    
    # Auto-join the player with their username for stat tracking
    game_service.join_game(db, room_id, client_id=current_user.username, username=current_user.username)
    
    # Fetch final state from DB to return as GameInfo
    db_game = crud.game.get_game_by_room(db, room_id)
    return db_game


@router.post("/move", response_model=dict)
def make_move(
    room_id: str,
    move: Move,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Make a move in a game session.
    """
    result = game_service.make_move(
        db,
        room_id, 
        current_user.username, 
        move.row, 
        move.col
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
        
    return result


@router.get("/{room_id}/chat", response_model=ChatHistory)
def get_chat_history(
    room_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get chat history for a specific room.
    """
    history = crud.chat.get_room_chat_history(db, room_id=room_id)
    messages = [
        ChatMessage(
            username=m.username,
            message=m.message,
            room_id=m.room_id,
            timestamp=m.timestamp.timestamp()
        ) for m in history
    ]
    return ChatHistory(messages=messages)
