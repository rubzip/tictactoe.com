import random
from dataclasses import dataclass
from app.services.cpu import Strategy,RandomStrategy, CustomStrategy, MinimaxStrategy



class MinMaxStrategy3(MinimaxStrategy):
    MAX_DEPTH = 3

class PerfectStrategt(MinimaxStrategy):
    MAX_DEPTH = 9


@dataclass
class Player:
    name: str
    strategy: Strategy
    elo: int = 1000

def run_simmulation(players, n_matches):
    matches = []
    for p1 in players:
        for p2 in players:
            if p1 == p2:
                continue
            matches.extend([(p1, p2) for _ in range(n_matches)])
    
    random.shuffle(matches)
    
