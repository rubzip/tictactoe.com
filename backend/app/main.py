from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.leaderboards import router as leaderboard_router
from app.api.ws.game_sockets import router as game_ws_router
from app.api.v1.game import router as game_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.challenges import router as challenges_router
from app.api.v1.notifications import router as notifications_router
from app.core.database import engine, Base, SessionLocal
from app.services.matchmaking_service import matchmaking_service
from app.core.exceptions import BaseAppException, NotFoundException, UnauthorizedException, ValidationException
from app import crud
from app.schemas.user import UserCreate
import asyncio

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend for tictactoe.com",
)

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    status_code = 400
    if isinstance(exc, NotFoundException):
        status_code = 404
    elif isinstance(exc, UnauthorizedException):
        status_code = 401
    elif isinstance(exc, ValidationException):
        status_code = 400
        
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "detail": exc.detail
        },
    )

# Initialize database
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    
    # Create test users if they don't exist
    db = SessionLocal()
    try:
        test_users = [
            ("user_1", "user_1@example.com", "password"),
            ("user_2", "user_2@example.com", "password")
        ]
        for username, email, password in test_users:
            if not crud.user.get_user(db, username=username):
                crud.user.create_user(
                    db, 
                    user_in=UserCreate(
                        username=username,
                        email=email,
                        password=password
                    )
                )
    finally:
        db.close()

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
