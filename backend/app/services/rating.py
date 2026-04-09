from sqlalchemy.orm import Session
from app.models.users import User


def calculate_elo(player_rating: float, opponent_rating: float, score: float, k_factor: int = 32) -> float:
    """
    Calculate the new Elo rating for a player.
    score: 1.0 for win, 0.5 for draw, 0.0 for loss.
    """
    expected_score = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
    new_rating = player_rating + k_factor * (score - expected_score)
    return new_rating


def update_user_game_stats(
    db: Session, 
    user_id: int, 
    is_win: bool = False, 
    is_draw: bool = False, 
    opponent_elo: float = 1000.0
):
    """
    Update user statistics and Elo after a game ends.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    user.played_games += 1
    
    score = 0.5 if is_draw else (1.0 if is_win else 0.0)
    if is_win:
        user.won_games += 1
    elif not is_draw:
        user.lost_games += 1
        
    # Calculate new Elo
    user.elo_rating = calculate_elo(user.elo_rating, opponent_elo, score)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
