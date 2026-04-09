import random

from app.core.constants import GameStatus, Player, DifficultyMode
from app.services.cpu import get_next_cpu_move
from app.services.game_engine import TicTacToeEngine
from app.services.ranking import EloEngine

"""
This script contains a simulation of a 'tournament' between the different CPU strategies.
"""

def play_game(diff1: DifficultyMode, diff2: DifficultyMode):
    board, turn, status = TicTacToeEngine.init_board()
    while status == GameStatus.KEEP_PLAYING:
        turn = TicTacToeEngine.get_current_player(board)
        difficulty = diff1 if turn == Player.X else diff2
        
        move = get_next_cpu_move(board, difficulty, turn)
        
        if move is None:
            break
        r, c = move
        board, turn, status = TicTacToeEngine.make_move(board, turn, turn, r, c)
    
    if status == GameStatus.WIN_X:
        return 1
    elif status == GameStatus.WIN_O:
        return 0
    return 0.5


def run_simulation(difficulties, n_matches):
    elo = {d.value: 1000. for d in difficulties}
    matches = []
    for d1 in difficulties:
        for d2 in difficulties:
            if d1 == d2:
                continue
            matches.extend([(d1, d2) for _ in range(n_matches)])
    random.shuffle(matches)
    
    for d1, d2 in matches:
        result = play_game(d1, d2)
        r1, r2 = EloEngine.compute(elo[d1.value], elo[d2.value], result)
        elo[d1.value] = r1
        elo[d2.value] = r2
    
    return elo

if __name__ == "__main__":
    difficulties = [d for d in DifficultyMode]
    results = run_simulation(difficulties, n_matches=10)
    print("\n\nCPU Comparison Results:")
    for i, (name, rating) in enumerate(sorted(results.items(), key=lambda x: x[1], reverse=True)):
        print(f"{i+1}. {name}: {rating:.2f}")
