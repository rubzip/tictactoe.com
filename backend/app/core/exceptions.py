from typing import Any


class BaseAppException(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, detail: Any = None):
        super().__init__(message)
        self.message = message
        self.detail = detail


class GameException(BaseAppException):
    """Base exception for game-related errors."""
    pass


class InvalidMoveException(GameException):
    """Raised when a move is invalid (out of bounds, wrong player, etc.)."""
    pass


class OccupiedCellException(InvalidMoveException):
    """Raised when a player tries to move to an already occupied cell."""
    def __init__(self, pos: Any):
        super().__init__(f"Cell at {pos} is already occupied", detail={"pos": pos})


class GameOverException(GameException):
    """Raised when an action is attempted on a game that is already over."""
    pass


class ConnectionException(BaseAppException):
    """Base exception for connection-related errors."""
    pass


class UnauthorizedException(BaseAppException):
    """Raised when an unauthorized action is attempted."""
    pass
