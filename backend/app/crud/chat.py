from sqlalchemy.orm import Session
from app.models.chat import Chat


from app.schemas.chat import ChatCreate


def create_chat_message(db: Session, chat_in: ChatCreate) -> Chat:
    db_chat = Chat(
        room_id=chat_in.room_id,
        username=chat_in.username,
        message=chat_in.message
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


def get_room_chat_history(db: Session, room_id: str, limit: int = 50) -> list[Chat]:
    return db.query(Chat).filter(Chat.room_id == room_id).order_by(Chat.timestamp.desc()).limit(limit).all()
