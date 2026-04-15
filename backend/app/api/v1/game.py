from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.game_service import game_service
from app.core.constants import DifficultyMode, Player
from app.api import deps
from app.schemas.game import Move, GameState, GameInfo
from app.schemas.chat import ChatHistory, ChatMessage
from app import crud
from app.models.users import User
from app.core.exceptions import RoomNotFoundException
import uuid
from typing import Optional

router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@router.post("/create", response_model=GameInfo)
def create_room(
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    """
    Create a new human vs human game room.
    """
    room_id = f"game_{uuid.uuid4().hex[:12]}"
    # get_or_create_session with default (no AI) will create a standard game
    game_service.get_or_create_session(db, room_id)
    
    db_game = crud.game.get_game_by_room(db, room_id)
    return db_game


@router.post("/ai/start", response_model=GameInfo)
def start_ai_game(
    difficulty: DifficultyMode,
    client_id: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
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
    
    # Auto-join the player. Use username if available, otherwise client_id or a random ID.
    effective_client_id = client_id or (current_user.username if current_user else f"guest_{uuid.uuid4().hex[:8]}")
    effective_username = current_user.username if current_user else None
    
    game_service.join_game(db, room_id, client_id=effective_client_id, username=effective_username)
    
    # Fetch state from DB to return as GameInfo
    db_game = crud.game.get_game_by_room(db, room_id)
    return db_game


@router.get("/{room_id}", response_model=GameInfo)
def get_game_info(
    room_id: str,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    """
    Get metadata for a specific game room.
    Useful for shared links before connecting via WebSocket.
    """
    db_game = crud.game.get_game_by_room(db, room_id)
    if not db_game:
        raise RoomNotFoundException(room_id)
    return db_game


@router.post("/move", response_model=dict)
def make_move(
    room_id: str,
    move: Move,
    client_id: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    """
    Make a move in a game session.
    """
    effective_client_id = client_id or (current_user.username if current_user else None)
    if not effective_client_id:
        raise HTTPException(status_code=400, detail="client_id or authentication required")

    return game_service.make_move(
        db,
        room_id, 
        effective_client_id, 
        move.row, 
        move.col
    )


@router.get("/{room_id}/chat", response_model=ChatHistory)
def get_chat_history(
    room_id: str,
    db: Session = Depends(deps.get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    """
    Get chat history for a specific room.
    """
    if not game_service.get_session(room_id):
        raise RoomNotFoundException(room_id)
        
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
