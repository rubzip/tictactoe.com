from fastapi import APIRouter

router = APIRouter(
    prefix="/game_end",
    tags=["game_end"]
)

@router.post("/win/{player_1_id}/{player_2_id}")
async def update_ranking_win(player_1_id: int, player_2_id: int) -> None:
    pass

@router.post("/draw/{player_1_id}/{player_2_id}")
async def update_ranking_draw(player_1_id: int, player_2_id: int) -> None:
    pass

@router.post("/lose/{player_1_id}/{player_2_id}")
async def update_ranking_lose(player_1_id: int, player_2_id: int) -> None:
    pass
