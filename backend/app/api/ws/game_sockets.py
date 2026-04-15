from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app import crud
from app.api.ws.connection_manager import manager
from app.services.game_service import game_service
from app.services.matchmaking_service import matchmaking_service
from app.schemas.ws_messages import MessageType
from app.schemas.notification import Notification as NotificationSchema
from app.core.database import SessionLocal
from app.models.users import User
import json

from app.core.config import settings
from app.core.exceptions import BaseAppException, RoomNotFoundException
from jose import jwt, JWTError

router = APIRouter()

def authenticate_websocket(db, token: str) -> Optional[User]:
    """Helper to authenticate a user from a JWT token."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username:
            return db.query(User).filter(User.username == username).first()
    except JWTError:
        pass
    return None

async def broadcast_game_state(room_id: str, session):
    """Utility to broadcast the current game state to a room."""
    await manager.broadcast_to_room({
        "type": MessageType.GAME_STATE,
        "payload": session.to_summary_dict()
    }, room_id)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: str = None):
    db = SessionLocal()
    user = authenticate_websocket(db, token)
    
    # We no longer close the connection if user is missing.
    # We accept the connection for anonymous users too.
    await manager.connect(websocket, client_id)
    room_id = None
    try:
        # 3. Message Loop
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                msg_type = message_data.get("type")
                payload = message_data.get("payload", {})

                if msg_type == MessageType.JOIN:
                    room_id = payload.get("room_id")
                    if room_id:
                        effective_username = user.username if user else None
                        player_role = game_service.join_game(db, room_id, client_id, username=effective_username)
                        await manager.join_room(client_id, room_id)
                        
                        session = game_service.get_or_create_session(db, room_id)
                        
                        await manager.send_personal_message({
                            "type": MessageType.JOIN,
                            "payload": {
                                "status": "success", 
                                "room_id": room_id,
                                "role": player_role,
                                "game_state": session.to_summary_dict()
                            }
                        }, client_id)
                        
                        # Also broadcast that someone joined
                        await broadcast_game_state(room_id, session)

                elif msg_type == MessageType.MOVE:
                    if not room_id:
                        room_id = payload.get("room_id")
                    
                    if room_id:
                        row = payload.get("row")
                        col = payload.get("col")
                        
                        result = game_service.make_move(db, room_id, client_id, row, col)
                        
                        if "error" in result:
                            await manager.send_personal_message({
                                "type": MessageType.ERROR,
                                "payload": result["error"]
                            }, client_id)
                        else:
                            await manager.broadcast_to_room({
                                "type": MessageType.GAME_STATE,
                                "payload": result
                            }, room_id)

                elif msg_type == MessageType.CHAT:
                    if not room_id:
                        room_id = payload.get("room_id")
                    
                    if room_id:
                        # Persist message
                        from app.schemas.chat import ChatCreate
                        effective_username = user.username if user else f"Guest_{client_id[:4]}"
                        crud.chat.create_chat_message(
                            db, 
                            chat_in=ChatCreate(
                                room_id=room_id, 
                                username=effective_username, 
                                message=payload.get("message")
                            )
                        )
                        
                        await manager.broadcast_to_room({
                            "type": MessageType.CHAT,
                            "payload": {
                                "client_id": client_id,
                                "username": effective_username,
                                "message": payload.get("message")
                            }
                        }, room_id)

                elif msg_type == MessageType.QUEUE_JOIN:
                    if not user:
                        await manager.send_personal_message({
                            "type": MessageType.ERROR,
                            "payload": "Authentication required for matchmaking"
                        }, client_id)
                        continue

                    await matchmaking_service.add_to_queue(
                        username=user.username,
                        client_id=client_id,
                        elo=int(user.elo_rating)
                    )
                    await manager.send_personal_message({
                        "type": MessageType.QUEUE_JOIN,
                        "payload": {"status": "searching"}
                    }, client_id)

                elif msg_type == MessageType.QUEUE_LEAVE:
                    if user:
                        await matchmaking_service.remove_from_queue(user.username)
                    await manager.send_personal_message({
                        "type": MessageType.QUEUE_LEAVE,
                        "payload": {"status": "left"}
                    }, client_id)

                elif msg_type == MessageType.SPECTATE:
                    room_id = payload.get("room_id")
                    if room_id:
                        effective_username = user.username if user else None
                        game_service.join_game(db, room_id, client_id, username=effective_username, as_spectator=True)
                        await manager.join_room(client_id, room_id)
                        
                        session = game_service.get_or_create_session(db, room_id)
                        await manager.send_personal_message({
                            "type": MessageType.SPECTATE,
                            "payload": {
                                "status": "success",
                                "room_id": room_id,
                                **session.to_summary_dict()
                            }
                        }, client_id)

            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": MessageType.ERROR,
                    "payload": "Invalid JSON"
                }, client_id)
            except BaseAppException as e:
                await manager.send_personal_message({
                    "type": MessageType.ERROR,
                    "payload": e.message
                }, client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        if user:
            await matchmaking_service.remove_from_queue(user.username)
        if room_id:
            import asyncio
            asyncio.create_task(manager.broadcast_to_room({
                "type": MessageType.ERROR,
                "payload": f"Player {user.username if user else client_id} has disconnected"
            }, room_id))
    except Exception as e:
        print(f"WebSocket Error: {e}")
        try:
            await websocket.close(code=1011)
        except:
            pass
    finally:
        db.close()
