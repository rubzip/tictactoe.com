from fastapi import APIRouter
from app.schemas.game import Move

router = APIRouter(
    prefix="/game",
    tags=["game"]
)


@router.get("/start")
async def start_game():
    pass

@router.post("/move")
async def make_move(move: Move):
    pass
