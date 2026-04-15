import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    # Create the database and the tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the tables to ensure a clean state for the next test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clean up overrides after test
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def user_token(client):
    """Fixture that registers a user and returns their auth token and headers."""
    user_data = {"username": "authtest", "email": "authtest@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=user_data)
    
    response = client.post(
        "/api/v1/auth/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    token = response.json()["access_token"]
    return {
        "username": user_data["username"],
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }
