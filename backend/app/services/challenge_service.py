import uuid
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.core.constants import ChallengeStatus
from app.crud.user import get_user
from app.crud.notification import create_notification
from app.models.notification import NotificationType


class ChallengeService:
    def create_challenge(self, db: Session, challenger_username: str, challenged_username: str) -> Challenge:
        # Validate users
        challenger = get_user(db, challenger_username)
        challenged = get_user(db, challenged_username)
        
        if not challenger or not challenged:
            raise ValueError("Challenger or challenged not found")
            
        if challenger_username == challenged_username:
            raise ValueError("You cannot challenge yourself")

        # Create challenge
        db_challenge = Challenge(
            challenger_username=challenger_username,
            challenged_username=challenged_username,
            room_id=str(uuid.uuid4()),
            status=ChallengeStatus.PENDING
        )
        db.add(db_challenge)
        db.commit()
        db.refresh(db_challenge)
        
        # Create notification for challenged user
        create_notification(
            db,
            username=challenged_username,
            message=f"You received a challenge from {challenger_username}",
            type=NotificationType.CHALLENGE,
            link_data=f"challenge_id={db_challenge.id}"
        )
        
        return db_challenge

    def get_challenge(self, db: Session, challenge_id: int) -> Challenge | None:
        return db.query(Challenge).filter(Challenge.id == challenge_id).first()

    def get_pending_challenges_for_user(self, db: Session, username: str) -> list[Challenge]:
        return db.query(Challenge).filter(
            Challenge.challenged_username == username,
            Challenge.status == ChallengeStatus.PENDING
        ).all()

    def update_challenge_status(self, db: Session, challenge_id: int, status: ChallengeStatus) -> Challenge | None:
        db_challenge = self.get_challenge(db, challenge_id)
        if db_challenge:
            db_challenge.status = status
            db.commit()
            db.refresh(db_challenge)
            
            # If accepted, we might want to pre-initialize the game
            if status == ChallengeStatus.ACCEPTED:
                from app.services.game_service import game_service
                game_service.get_or_create_session(db, room_id=db_challenge.room_id)
                
                # Notify challenger
                create_notification(
                    db,
                    username=db_challenge.challenger_username,
                    message=f"{db_challenge.challenged_username} ha aceptado tu reto",
                    type=NotificationType.INFO,
                    link_data=f"room_id={db_challenge.room_id}"
                )
                
        return db_challenge

challenge_service = ChallengeService()