from fastapi import APIRouter
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

USERS = [
    User(id=1, username="alice", email="alice@example.com"),
    User(id=2, username="bob", email="bob@example.com"),
    User(id=3, username="charlie", email="charlie@example.com")
]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int) -> User:
    pass

@router.post("/", response_model=User)
async def create_user(user: UserCreate) -> User:
    pass

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate) -> User:
    pass

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int) -> User:
    pass
