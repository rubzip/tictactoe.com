from sqlalchemy.orm import Session
from app.models.users import User
from app.models.ranking import Ranking, RankingItem
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_ranking(db: Session, page: int = 1, page_size: int = 10) -> list[User]:
    pass
