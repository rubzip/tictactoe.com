from sqlalchemy.orm import Session
from app.models.users import User
from sqlalchemy import desc

def get_ranking(db: Session, limit: int = 10, offset: int = 0) -> list[User]:
    return db.query(User).order_by(desc(User.elo_rating)).limit(limit).offset(offset).all()
