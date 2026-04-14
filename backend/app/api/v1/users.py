from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.users import User
from app.schemas.user import User as UserSchema
from app.schemas.game import MatchHistory

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)):
    """
    Get current logged in user.
    """
    return current_user


@router.patch("/me", response_model=UserSchema)
def update_user_me(
    user_in: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update my profile.
    """
    return crud.user.update_user(db, db_user=current_user, user_in=user_in)


@router.get("/{username}", response_model=UserSchema)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a specific user by username.
    """
    user = crud.user.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{username}/history", response_model=MatchHistory)
def read_user_match_history(
    username: str, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    """
    Get match history for a specific user.
    """
    matches = crud.game.get_user_match_history(db, username=username, limit=limit)
    return MatchHistory(matches=matches)

# Removed read_user_by_username redundant endpoint
