import pytest

def test_create_challenge_success(client, user_token):
    # Register another user to challenge
    challenged_user = {"username": "challenged", "email": "challenged@example.com", "password": "password"}
    client.post("/api/v1/auth/register", json=challenged_user)
    
    response = client.post(
        "/api/v1/challenges/",
        headers=user_token["headers"],
        json={"challenged_username": "challenged"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["challenger_username"] == user_token["username"]
    assert data["challenged_username"] == "challenged"
    assert data["status"] == "PENDING"

def test_challenge_yourself(client, user_token):
    response = client.post(
        "/api/v1/challenges/",
        headers=user_token["headers"],
        json={"challenged_username": user_token["username"]}
    )
    assert response.status_code == 400
    assert response.json()["error"] == "SelfChallengeException"

def test_challenge_nonexistent_user(client, user_token):
    response = client.post(
        "/api/v1/challenges/",
        headers=user_token["headers"],
        json={"challenged_username": "ghost"}
    )
    assert response.status_code == 404
    assert response.json()["error"] == "UserNotFoundException"

def test_get_pending_challenges(client, user_token):
    # Register other user and challenge current user
    other_user = {"username": "other", "email": "other@example.com", "password": "password"}
    client.post("/api/v1/auth/register", json=other_user)
    
    # Login as other user to send challenge
    login_resp = client.post(
        "/api/v1/auth/token",
        data={"username": "other", "password": "password"}
    )
    other_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}
    
    client.post(
        "/api/v1/challenges/",
        headers=other_headers,
        json={"challenged_username": user_token["username"]}
    )
    
    # Check pending challenges for current user
    response = client.get("/api/v1/challenges/pending", headers=user_token["headers"])
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["challenger_username"] == "other"

def test_accept_challenge(client, user_token):
    # Other user challenges current user
    other_user = {"username": "other", "email": "other@example.com", "password": "password"}
    client.post("/api/v1/auth/register", json=other_user)
    login_resp = client.post("/api/v1/auth/token", data={"username": "other", "password": "password"})
    other_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}
    
    challenge_resp = client.post(
        "/api/v1/challenges/",
        headers=other_headers,
        json={"challenged_username": user_token["username"]}
    )
    challenge_id = challenge_resp.json()["id"]
    
    # Accept challenge
    response = client.post(
        f"/api/v1/challenges/{challenge_id}/accept",
        headers=user_token["headers"]
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ACCEPTED"
