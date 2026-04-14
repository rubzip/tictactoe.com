from typing import Tuple
from app.core.constants import GameResult, GameStatus

class EloEngine:
    @staticmethod
    def compute(elo_x: float, elo_o: float, game_result: GameResult, k: float = 32.0) -> Tuple[float, float]:
        """
        Computes new Elo of 2 players.
        
        :param elo_x: actual Elo player X
        :param elo_o: actual Elo player O
        :param game_result: Game result
        :param k: Factor K (volatility). 32 is standard.
        """
        if game_result == GameStatus.WIN_X:
            score_x = 1.0
        elif game_result == GameStatus.DRAW:
            score_x = 0.5
        else:
            score_x = 0.0

        e1, e2 = EloEngine.compute_probability(elo_x, elo_o)
        score_o = 1.0 - score_x

        new_elo_x = elo_x + k * (score_x - e1)
        new_elo_o = elo_o + k * (score_o - e2)

        return new_elo_x, new_elo_o

    @staticmethod
    def compute_q(x: float) -> float:
        """
        Computes the expected score of a player with Elo rating x.
        """
        return 10. ** (x / 400.)
    
    @staticmethod
    def compute_probability(r1: float, r2: float) -> Tuple[float, float]:
        """
        Computes the expected score of 2 players.
        """
        q1 = EloEngine.compute_q(r1)
        q2 = EloEngine.compute_q(r2)

        e1 = q1 / (q1 + q2)
        e2 = q2 / (q1 + q2)

        return e1, e2
