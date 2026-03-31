from typing import List
from pydantic import BaseModel

class RankingItem(BaseModel):
    pos: int
    user: str
    elo: int

class Ranking(BaseModel):
    items: List[RankingItem]
