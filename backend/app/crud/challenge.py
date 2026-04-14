import uuid
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.core.constants import ChallengeStatus
from app.schemas.challenge import ChallengeCreate


def create_challenge(db: Session, challenger_username: str, challenged_username: str) -> Challenge:
    db_challenge = Challenge(
        challenger_username=challenger_username,
        challenged_username=challenged_username,
        room_id=str(uuid.uuid4()),
        status=ChallengeStatus.PENDING
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_challenge(db: Session, challenge_id: int) -> Challenge | None:
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()


def get_pending_challenges_for_user(db: Session, username: str) -> list[Challenge]:
    return db.query(Challenge).filter(
        Challenge.challenged_username == username,
        Challenge.status == ChallengeStatus.PENDING
    ).all()


def update_challenge_status(db: Session, challenge_id: int, status: ChallengeStatus) -> Challenge | None:
    db_challenge = get_challenge(db, challenge_id)
    if db_challenge:
        db_challenge.status = status
        db.commit()
        db.refresh(db_challenge)
    return db_challenge
