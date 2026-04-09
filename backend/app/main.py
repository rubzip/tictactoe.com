from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.leaderboards import router as leaderboard_router
from app.api.ws.game_sockets import router as game_ws_router
from app.api.v1.game import router as game_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.challenges import router as challenges_router
from app.core.database import engine, Base

app = FastAPI(
    title="TicTacToe API",
    description="Backend for tictactoe.com",
    version="0.1.0"
)

# Initialize database
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(leaderboard_router, prefix="/api/v1")
app.include_router(game_ws_router)
app.include_router(game_router, prefix="/api/v1")
app.include_router(challenges_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")



@app.get("/")
async def root():
    return {"message": "Welcome to tictactoe.com API"}
