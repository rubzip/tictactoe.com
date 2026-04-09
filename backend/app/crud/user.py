from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: dict) -> User:
    for field in user_in:
        if field == "password":
            db_user.hashed_password = get_password_hash(user_in[field])
        else:
            setattr(db_user, field, user_in[field])
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
