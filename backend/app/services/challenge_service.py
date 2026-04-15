import uuid
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.core.constants import ChallengeStatus
from app.core.exceptions import UserNotFoundException, SelfChallengeException
from app import crud
from app.models.notification import NotificationType


class ChallengeService:
    def create_challenge(self, db: Session, challenger_username: str, challenged_username: str) -> Challenge:
        # Validate users
        challenger = crud.user.get_user(db, challenger_username)
        challenged = crud.user.get_user(db, challenged_username)
        
        if not challenger:
            raise UserNotFoundException(challenger_username)
        if not challenged:
            raise UserNotFoundException(challenged_username)
            
        if challenger_username == challenged_username:
            raise SelfChallengeException()

        # Create challenge
        from app.schemas.challenge import ChallengeCRUDCreate
        db_challenge = crud.challenge.create_challenge(
            db, 
            challenge_in=ChallengeCRUDCreate(
                challenger_username=challenger_username,
                challenged_username=challenged_username,
                room_id=str(uuid.uuid4())
            )
        )
        
        # Create notification for challenged user
        from app.schemas.notification import NotificationCreate
        crud.notification.create_notification(
            db,
            notification_in=NotificationCreate(
                username=challenged_username,
                message=f"You received a challenge from {challenger_username}",
                type=NotificationType.CHALLENGE,
                link_data=f"challenge_id={db_challenge.id}"
            )
        )
        
        return db_challenge

    def get_challenge(self, db: Session, challenge_id: int) -> Challenge | None:
        return crud.challenge.get_challenge(db, challenge_id)

    def get_pending_challenges_for_user(self, db: Session, username: str) -> list[Challenge]:
        return crud.challenge.get_pending_challenges_for_user(db, username=username)

    def update_challenge_status(self, db: Session, challenge_id: int, status: ChallengeStatus) -> Challenge | None:
        from app.schemas.challenge import ChallengeUpdate
        db_challenge = crud.challenge.update_challenge_status(db, challenge_id, ChallengeUpdate(status=status))
        if db_challenge:
            # If accepted, we might want to pre-initialize the game
            if status == ChallengeStatus.ACCEPTED:
                from app.services.game_service import game_service
                game_service.get_or_create_session(db, room_id=db_challenge.room_id)
                
                # Notify challenger
                from app.schemas.notification import NotificationCreate
                crud.notification.create_notification(
                    db,
                    notification_in=NotificationCreate(
                        username=db_challenge.challenger_username,
                        message=f"{db_challenge.challenged_username} ha aceptado tu reto",
                        type=NotificationType.INFO,
                        link_data=f"room_id={db_challenge.room_id}"
                    )
                )
                
        return db_challenge

challenge_service = ChallengeService()