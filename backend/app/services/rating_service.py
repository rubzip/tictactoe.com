from typing import Optional
from sqlalchemy.orm import Session
from app.game_logic.elo_engine import EloEngine
from app.core.constants import GameResult, GameStatus
from app.crud.user import get_user, update_user
from app.models.users import User

class RatingService:
    @staticmethod
    def update_user_game_stats(
        db: Session, 
        username_x: Optional[str], 
        username_o: Optional[str], 
        game_result: GameStatus
    ):
        # 1. Fetch users (handle bots)
        user_x = get_user(db, username_x) if username_x else None
        user_o = get_user(db, username_o) if username_o else None

        # 2. Update Elo only if both are humans
        if user_x and user_o:
            new_elo_x, new_elo_o = EloEngine.compute(user_x.elo_rating, user_o.elo_rating, game_result)
            user_x.elo_rating = new_elo_x
            user_o.elo_rating = new_elo_o

        # 3. Update basic stats for each human player
        for user, role in [(user_x, GameStatus.WIN_X), (user_o, GameStatus.WIN_O)]:
            if not user:
                continue
            
            user.played_games += 1
            if game_result == role:
                user.won_games += 1
            elif game_result == GameStatus.DRAW:
                pass # Draw doesn't increment won/lost
            else:
                user.lost_games += 1
            
            db.add(user)

        db.commit()

rating_service = RatingService()
