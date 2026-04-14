from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.users import User
from app.core.constants import ChallengeStatus
from app.schemas.challenge import ChallengeCreate, ChallengeInfo
from app.core.database import get_db
from app.services.challenge_service import challenge_service

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
    try:
        return challenge_service.create_challenge(
            db, 
            challenger_username=current_user.username, 
            challenged_username=challenge_in.challenged_username
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/pending", response_model=List[ChallengeInfo])
def get_pending_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all pending challenges for the current user.
    """
    return challenge_service.get_pending_challenges_for_user(db, username=current_user.username)


@router.post("/{challenge_id}/accept", response_model=ChallengeInfo)
def accept_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Accept a challenge.
    """
    challenge = challenge_service.get_challenge(db, challenge_id)
    if not challenge or challenge.challenged_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    if challenge.status != ChallengeStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge is already {challenge.status.value}"
        )
    
    # Update challenge status (Service handles game initialization if status is ACCEPTED)
    updated_challenge = challenge_service.update_challenge_status(db, challenge_id, ChallengeStatus.ACCEPTED)
    return updated_challenge
