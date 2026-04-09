from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.leaderboards import router as leaderboard_router
from app.api.ws.game_sockets import router as game_ws_router

app = FastAPI(
    title="TicTacToe API",
    description="Backend for tictactoe.com",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leaderboard_router, prefix="/api/v1")
app.include_router(game_ws_router)

@app.get("/")
async def root():
    return {"message": "Welcome to tictactoe.com API"}
