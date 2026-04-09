from fastapi import APIRouter
from app.schemas.ranking import Ranking, RankingItem

router = APIRouter(
    prefix="/leaderboards",
    tags=["leaderboards"]
)

MOCK_RANKING = [
    RankingItem(pos=1, user="Magnus Carlsen", elo=2882),
    RankingItem(pos=2, user="Garry Kasparov", elo=2851),
    RankingItem(pos=3, user="Fabiano Caruana", elo=2844),
    RankingItem(pos=4, user="Levon Aronian", elo=2830),
    RankingItem(pos=5, user="Wesley So", elo=2822),
    RankingItem(pos=6, user="Hikaru Nakamura", elo=2816),
    RankingItem(pos=7, user="Ding Liren", elo=2799),
    RankingItem(pos=8, user="Anish Giri", elo=2797),
    RankingItem(pos=9, user="Ian Nepomniachtchi", elo=2792),
    RankingItem(pos=10, user="Viswanathan Anand", elo=2791),
    RankingItem(pos=11, user="Bobby Fischer", elo=2785),
    RankingItem(pos=12, user="Mikhail Tal", elo=2705),
]


@router.get("/", response_model=Ranking)
async def get_leaderboard(page: int = 1, page_size: int = 10) -> Ranking:
    """
    Get the top players and their Elo ratings.
    """
    return Ranking(items=MOCK_RANKING[(page - 1) * page_size: page * page_size])
