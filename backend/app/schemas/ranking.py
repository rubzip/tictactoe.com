from typing import List, Any
from pydantic import BaseModel, field_validator


class RankingItem(BaseModel):
    pos: int
    username: str
    elo: int

    @field_validator("elo", mode="before")
    @classmethod
    def round_elo(cls, v: Any) -> int:
        if isinstance(v, float):
            return int(round(v))
        return v


class Ranking(BaseModel):
    items: List[RankingItem]
