import pytest

def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" not in data # Should be excluded or use User schema

def test_register_duplicate_username(client):
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Duplicate registration
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "other@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "UserAlreadyExistsException"

def test_login_success(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    # Login
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "testuser", "password": "password123"} # OAuth2 uses form data
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["error"] == "InvalidCredentialsException"
