from enum import StrEnum


class GameStatus(StrEnum):
    WIN_X = "X_WINS"
    WIN_O = "O_WINS"
    DRAW = "DRAW"
    KEEP_PLAYING = "KEEP_PLAYING"


class Player(StrEnum):
    NONE = ""
    X = "X"
    O = "O"
