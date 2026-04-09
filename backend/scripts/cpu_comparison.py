import random

from app.core.constants import GameStatus, Player
from app.services.cpu import EasyCPU, MediumCPU, HardCPU, PerfectCPU
from app.services.game_engine import TicTacToeEngine
from app.services.strategies import Strategy 
from app.services.ranking import EloEngine

"""
This script contains a simulation of a 'tournament' between the different CPU strategies.
"""

def play_game(cpu1: Strategy, cpu2: Strategy):
    board, turn, status = TicTacToeEngine.init_board()
    while status == GameStatus.KEEP_PLAYING:
        turn = TicTacToeEngine.get_current_player(board)
        if turn == Player.X:
            move = cpu1.get_move(board, turn)
        else:
            move = cpu2.get_move(board, turn)
        if move is None:
            break
        r, c = move
        board, turn, status = TicTacToeEngine.make_move(board, turn, turn, r, c)
    if status == GameStatus.WIN_X:
        return 1
    elif status == GameStatus.WIN_O:
        return 0
    return 0.5


def run_simulation(cpu_strategies, n_matches):
    elo = {name: 1000 for name in cpu_strategies}
    matches = []
    for p1 in cpu_strategies:
        for p2 in cpu_strategies:
            if p1 == p2:
                continue
            matches.extend([(p1, p2) for _ in range(n_matches)])
    random.shuffle(matches)
    
    for p1, p2 in matches:
        result = play_game(cpu_strategies[p1], cpu_strategies[p2])
        r1, r2 = EloEngine.compute(elo[p1], elo[p2], result)
        elo[p1] = r1
        elo[p2] = r2
    
    return elo

if __name__ == "__main__":
    cpu = {
        "EasyCPU": EasyCPU,
        "MediumCPU": MediumCPU,
        "HardCPU": HardCPU,
        "PerfectCPU": PerfectCPU
    }
    results = run_simulation(cpu, n_matches=10)
    print("\n\nCPU Comparison Results:")
    for i, (name, rating) in enumerate(sorted(results.items(), key=lambda x: x[1], reverse=True)):
        print(f"{i+1}. {name}: {rating:.2f}")
