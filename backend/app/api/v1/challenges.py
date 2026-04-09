from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.api import deps
from app.models.users import User
from app.core.constants import ChallengeStatus
from app.schemas.challenge import ChallengeCreate, ChallengeInfo
from app.core.database import get_db

router = APIRouter(
    prefix="/challenges",
    tags=["challenges"]
)


@router.post("/", response_model=ChallengeInfo, status_code=status.HTTP_201_CREATED)
def create_challenge(
    challenge_in: ChallengeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Challenge another player.
    """
    if challenge_in.challenged_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot challenge yourself"
        )
    
    # Check if opponent exists
    opponent = crud.get_user(db, user_id=challenge_in.challenged_id)
    if not opponent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opponent not found"
        )
    
    return crud.challenge.create_challenge(
        db, 
        challenger_id=current_user.id, 
        challenged_id=challenge_in.challenged_id
    )


@router.get("/pending", response_model=List[ChallengeInfo])
def get_pending_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all pending challenges for the current user.
    """
    return crud.challenge.get_pending_challenges_for_user(db, user_id=current_user.id)


@router.post("/{challenge_id}/accept", response_model=ChallengeInfo)
def accept_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Accept a challenge.
    """
    challenge = crud.challenge.get_challenge(db, challenge_id)
    if not challenge or challenge.challenged_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    if challenge.status != ChallengeStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge is already {challenge.status.value}"
        )
    
    # Update challenge status
    updated_challenge = crud.challenge.update_challenge_status(db, challenge_id, ChallengeStatus.ACCEPTED)
    
    # Initialize game record in DB
    from app.services.game_service import game_service
    game_service.get_or_create_session(db, room_id=updated_challenge.room_id)
    
    return updated_challenge
