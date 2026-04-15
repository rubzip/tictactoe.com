import pytest

def test_read_user_me(client, user_token):
    response = client.get("/api/v1/users/me", headers=user_token["headers"])
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_token["username"]

def test_read_user_me_unauthorized(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401 # FastAPI's OAuth2 default

def test_update_user_me_email(client, user_token):
    response = client.patch(
        "/api/v1/users/me",
        headers=user_token["headers"],
        json={"email": "newemail@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newemail@example.com"

def test_update_user_me_password(client, user_token):
    # Update password
    response = client.patch(
        "/api/v1/users/me",
        headers=user_token["headers"],
        json={"password": "newpassword123"}
    )
    assert response.status_code == 200
    
    # Try logging in with new password
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": user_token["username"], "password": "newpassword123"}
    )
    assert login_response.status_code == 200

def test_read_other_user(client, user_token):
    # Register another user
    other_user = {"username": "other", "email": "other@example.com", "password": "password"}
    client.post("/api/v1/auth/register", json=other_user)
    
    response = client.get(f"/api/v1/users/other")
    assert response.status_code == 200
    assert response.json()["username"] == "other"

def test_read_nonexistent_user(client):
    response = client.get("/api/v1/users/nonexistent")
    assert response.status_code == 404
    assert response.json()["error"] == "UserNotFoundException"
