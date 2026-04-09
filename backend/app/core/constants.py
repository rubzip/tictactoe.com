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

class ConnectionStatus(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"
    DISCONNECTED = "DISCONNECTED"

class DifficultyMode(StrEnum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"
