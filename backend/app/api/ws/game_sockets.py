from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.ws.connection_manager import manager
from app.services.game_service import game_service
from app.schemas.ws_messages import MessageType
from app.core.database import SessionLocal
from app.models.users import User
from app import deps
import json

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    room_id = None
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                msg_type = message_data.get("type")
                payload = message_data.get("payload", {})

                if msg_type == MessageType.JOIN:
                    room_id = payload.get("room_id")
                    if room_id:
                        # Try to look up user for stat tracking
                        user = db.query(User).filter(User.username == client_id).first()
                        user_id = user.id if user else None
                        
                        player_role = game_service.join_game(db, room_id, client_id, user_id=user_id)
                        await manager.join_room(client_id, room_id)
                        
                        # Get current state (session will already exist if started via REST)
                        session = game_service.get_or_create_session(db, room_id)
                        
                        await manager.send_personal_message({
                            "type": MessageType.JOIN,
                            "payload": {
                                "status": "success", 
                                "room_id": room_id,
                                "role": player_role,
                                "is_ai_game": session.is_ai_game,
                                "difficulty": session.ai_difficulty
                            }
                        }, client_id)
                        
                        # Notify the room about the current state
                        await manager.broadcast_to_room({
                            "type": MessageType.GAME_STATE,
                            "payload": {
                                "board": session.board,
                                "turn": session.turn,
                                "status": session.status,
                                "players": list(session.players.keys())
                            }
                        }, room_id)

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
                            # If it's an AI game, the result contains the board after BOTH moves
                            await manager.broadcast_to_room({
                                "type": MessageType.GAME_STATE,
                                "payload": result
                            }, room_id)

                elif msg_type == MessageType.CHAT:
                    if not room_id:
                        room_id = payload.get("room_id")
                    
                    if room_id:
                        await manager.broadcast_to_room({
                            "type": MessageType.CHAT,
                            "payload": {
                                "client_id": client_id,
                                "message": payload.get("message")
                            }
                        }, room_id)

            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": MessageType.ERROR,
                    "payload": "Invalid JSON"
                }, client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    finally:
        db.close()
