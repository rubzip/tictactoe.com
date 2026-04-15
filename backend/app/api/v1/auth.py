from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.auth import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    user = crud.user.get_user(db, username=user_in.username)
    if user:
        raise UserAlreadyExistsException("Username already registered")

    user = crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise UserAlreadyExistsException("Email already registered")
    
    # Create new user
    return crud.user.create_user(db, user_in=user_in)


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user
    user = crud.user.get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsException()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
