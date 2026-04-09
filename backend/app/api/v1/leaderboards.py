from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ranking import Ranking, RankingItem
from app.api import deps
from app.models.users import User

router = APIRouter(
    prefix="/leaderboards",
    tags=["leaderboards"]
)


@router.get("/", response_model=Ranking)
async def get_leaderboard(
    page: int = 1, 
    page_size: int = 10,
    db: Session = Depends(deps.get_db)
) -> Ranking:
    """
    Get the top players and their Elo ratings.
    """
    total_users = db.query(User).count()
    users = db.query(User).order_by(User.elo_rating.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    items = []
    for i, user in enumerate(users):
        items.append(RankingItem(
            pos=((page - 1) * page_size) + i + 1,
            user=user.username,
            elo=int(user.elo_rating)
        ))
        
    return Ranking(items=items)
