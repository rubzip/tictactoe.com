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


class InvalidCredentialsException(UnauthorizedException):
    """Raised when login credentials are incorrect."""
    def __init__(self):
        super().__init__("Incorrect username or password")


class ValidationException(BaseAppException):
    """Base exception for validation errors."""
    pass


class UserAlreadyExistsException(ValidationException):
    """Raised when a user with the same username or email already exists."""
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundException(BaseAppException):
    """Base exception for resource not found errors."""
    pass


class UserNotFoundException(NotFoundException):
    """Raised when a user is not found."""
    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found", detail={"username": username})


class ChallengeNotFoundException(NotFoundException):
    """Raised when a challenge is not found."""
    def __init__(self, challenge_id: int):
        super().__init__(f"Challenge with ID {challenge_id} not found", detail={"challenge_id": challenge_id})


class RoomNotFoundException(NotFoundException):
    """Raised when a game room is not found."""
    def __init__(self, room_id: str):
        super().__init__(f"Room '{room_id}' not found", detail={"room_id": room_id})


class NotificationNotFoundException(NotFoundException):
    """Raised when a notification is not found."""
    def __init__(self, notification_id: int):
        super().__init__(f"Notification with ID {notification_id} not found", detail={"notification_id": notification_id})


class SelfChallengeException(ValidationException):
    """Raised when a user tries to challenge themselves."""
    def __init__(self):
        super().__init__("You cannot challenge yourself")


class InvalidDifficultyException(ValidationException):
    """Raised when an invalid difficulty level is provided."""
    def __init__(self, difficulty: str):
        super().__init__(f"Invalid difficulty: {difficulty}", detail={"difficulty": difficulty})
