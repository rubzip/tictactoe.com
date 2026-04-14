from sqlalchemy.orm import Session
from app.models.chat import Chat


def create_chat_message(db: Session, room_id: str, username: str, message: str) -> Chat:
    db_chat = Chat(
        room_id=room_id,
        username=username,
        message=message
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_room_chat_history(db: Session, room_id: str, limit: int = 50) -> list[Chat]:
    return db.query(Chat).filter(Chat.room_id == room_id).order_by(Chat.timestamp.desc()).limit(limit).all()
