import uuid
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.core.constants import ChallengeStatus
from app.schemas.challenge import ChallengeCRUDCreate, ChallengeUpdate


def create_challenge(db: Session, challenge_in: ChallengeCRUDCreate) -> Challenge:
    db_challenge = Challenge(
        challenger_username=challenge_in.challenger_username,
        challenged_username=challenge_in.challenged_username,
        room_id=challenge_in.room_id,
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


def update_challenge_status(db: Session, challenge_id: int, challenge_in: ChallengeUpdate) -> Challenge | None:
    db_challenge = get_challenge(db, challenge_id)
    if db_challenge:
        db_challenge.status = challenge_in.status
        db.commit()
        db.refresh(db_challenge)
    return db_challenge
