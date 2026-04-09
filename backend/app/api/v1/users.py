from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.users import User
from app.schemas.user import User as UserSchema

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


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by id.
    """
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/username/{username}", response_model=UserSchema)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a specific user by username.
    """
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
