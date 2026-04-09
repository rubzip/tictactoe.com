import uuid
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.core.constants import ChallengeStatus
from app.schemas.challenge import ChallengeCreate


def create_challenge(db: Session, challenger_id: int, challenged_id: int) -> Challenge:
    db_challenge = Challenge(
        challenger_id=challenger_id,
        challenged_id=challenged_id,
        room_id=str(uuid.uuid4()),
        status=ChallengeStatus.PENDING
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_challenge(db: Session, challenge_id: int) -> Challenge | None:
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()


def get_pending_challenges_for_user(db: Session, user_id: int) -> list[Challenge]:
    return db.query(Challenge).filter(
        Challenge.challenged_id == user_id,
        Challenge.status == ChallengeStatus.PENDING
    ).all()


def update_challenge_status(db: Session, challenge_id: int, status: ChallengeStatus) -> Challenge | None:
    db_challenge = get_challenge(db, challenge_id)
    if db_challenge:
        db_challenge.status = status
        db.commit()
        db.refresh(db_challenge)
    return db_challenge
