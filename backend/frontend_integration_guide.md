# Frontend Integration Guide - TicTacToe.com

This document provides all the necessary information for a frontend developer to integrate with the TicTacToe.com backend.

## 1. Authentication

The API uses JWT Bearer tokens for authentication.

### Register
*   **Endpoint**: `POST /api/v1/auth/register`
*   **Payload**:
    ```json
    {
      "username": "user1",
      "email": "user1@example.com",
      "password": "password123",
      "avatar_url": "https://..." // optional
    }
    ```

### Login (Token Generation)
*   **Endpoint**: `POST /api/v1/auth/token` (Form Data)
*   **Body**: `username`, `password`
*   **Response**:
    ```json
    {
      "access_token": "...",
      "token_type": "bearer"
    }
    ```

## 2. Real-time Gameplay (WebSockets)

WebSocket endpoints handle state synchronization, matchmaking, and moves.

### Connection
*   **URL**: `ws://localhost:8000/ws/{token}`
    *   `token`: Use the JWT token received during login.

### Message Protocol
All messages follow this structure:
```json
{
  "type": "MESSAGE_TYPE",
  "payload": { ... }
}
```

#### Client to Server
| Type | Payload Example | Description |
| :--- | :--- | :--- |
| `QUEUE_JOIN` | `{}` | Join the matchmaking queue. |
| `QUEUE_LEAVE` | `{}` | Leave the matchmaking queue. |
| `MOVE` | `{"row": 0, "col": 1}` | Submit a move for the current turn. |
| `CHAT` | `{"message": "Hello!"}` | Send a message to the room. |
| `JOIN` | `{"room_id": "..."}` | Rejoin or join a specific room. Returns full state. |

#### Server to Client
| Type | Payload Example | Description |
| :--- | :--- | :--- |
| `MATCH_FOUND` | `{"room_id": "...", "opponent": "user2"}` | Matchmaking found a game. |
| `JOIN` | `{"status": "success", "room_id": "...", "role": "X", "game_state": {...}}` | Response to JOIN. Includes full state. |
| `GAME_STATE` | `{ "board": [...], "turn": "X", "status": "KEEP_PLAYING", ... }` | Generic board and game state update. |
| `ERROR` | `"Invalid move"` | Error message. |
| `CHAT` | `{"username": "user1", "message": "...", "timestamp": ...}` | Broadcasted room message. |

---

## 3. REST API Reference

### Challenges
*   `GET /api/v1/challenges/pending`: Retrieve pending challenges for you.
*   `POST /api/v1/challenges/`: Challenge another player. Payload: `{"challenged_username": "..."}`.
*   `POST /api/v1/challenges/{id}/accept`: Accept a challenge.
*   `POST /api/v1/challenges/{id}/decline`: Decline a challenge.

### Users & Leaderboard
*   `GET /api/v1/users/me`: Current user profile (authenticated).
*   `GET /api/v1/users/{username}/match-history`: Match history for a user.
*   `GET /api/v1/leaderboards/`: Top players sorted by Elo.

### Games
*   `GET /api/v1/game/{room_id}`: Get metadata for a room (players, status, AI). Used for shared links.
*   `GET /api/v1/game/{room_id}/chat`: Get chat history for a persistent game room.

---

## 4. Common Data Models

### User Info
```json
{
  "username": "user1",
  "email": "...",
  "avatar_url": "...",
  "elo_rating": 1200,
  "wins": 5,
  "losses": 2,
  "draws": 1
}
```

### Game State (returned in GAME_STATE WebSocket message)
```json
{
  "room_id": "...",
  "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
  "turn": "X", // or "O"
  "status": "KEEP_PLAYING", // "X_WINS", "O_WINS", "DRAW"
  "win_line": [], // [[0,0], [0,1], [0,2]] if finished
  "player_x_username": "user1",
  "player_o_username": "user2",
  "is_ai_game": false
}
```

## 5. Error Handling
The backend uses a centralized exception handler. Errors return:
```json
{
  "error": "ExceptionClassName",
  "message": "Human readable message",
  "detail": { ... }
}
```
Common codes: `401 Unauthorized`, `404 Not Found`, `400 ValidationException`.
