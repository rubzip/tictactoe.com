from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.leaderboards import router as leaderboard_router
from app.api.ws.game_sockets import router as game_ws_router
from app.api.v1.game import router as game_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.challenges import router as challenges_router
from app.api.v1.notifications import router as notifications_router
from app.core.database import engine, Base
from app.services.matchmaking_service import matchmaking_service
import asyncio

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend for tictactoe.com",
)

# Initialize database
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    # Start matchmaking background task
    asyncio.create_task(matchmaking_service.run_matchmaker())

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
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
app.include_router(notifications_router, prefix="/api/v1")



@app.get("/")
async def root():
    return {"message": "Welcome to tictactoe.com API"}
