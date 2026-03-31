from app.core.constants import Player, GameStatus
from app.core.types import UsablePlayer, BoardType
from app.core.exceptions import InvalidMoveException, OccupiedCellException, GameOverException

from dataclasses import dataclass


@dataclass
class BoardEfficient:
    mask_x: list[bool]
    mask_o: list[bool]

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

class TicTacToeEngineEfficient:
    """TicTacToe Engine. Always starts X."""

    @staticmethod
    def init_board() -> tuple[BoardEfficient, Player, GameStatus]:
        board = BoardEfficient(
            mask_x = [False] * 9,
            mask_o = [False] * 9
        )
        return board, Player.X, GameStatus.KEEP_PLAYING
    
    @staticmethod
    def get_game_status(board: BoardEfficient) -> GameStatus:
        for p in (Player.X, Player.O):
            mask = board.mask_x if p == Player.X else board.mask_o
            for c in WINNING_COMBINATIONS:
                if mask[c[0]] and mask[c[1]] and mask[c[2]]:
                    return GameStatus.WIN_X if p == Player.X else GameStatus.WIN_O

        if all(pos_x or pos_o for pos_x, pos_o in zip(board.mask_x, board.mask_o)):
            return GameStatus.DRAW

        return GameStatus.KEEP_PLAYING
    
    @staticmethod
    def validate_board(board: BoardEfficient, turn: Player):
        status = TicTacToeEngineEfficient.get_game_status(board)
        
        x_count = sum(board.mask_x)
        o_count = sum(board.mask_o)
        
        if not (o_count + 1 >= x_count >= o_count):
            raise InvalidMoveException("Invalid board: turn count imbalance.")
        if x_count == o_count and turn != Player.X:
            raise InvalidMoveException("Invalid board: turn must be X.")
        if x_count > o_count and turn != Player.O:
            raise InvalidMoveException("Invalid board: turn must be O.")

        if status != GameStatus.KEEP_PLAYING:
            turn = Player.NONE
        elif turn == Player.NONE:
            raise InvalidMoveException("Game is ongoing; turn must be X or O.")
    
    @staticmethod
    def make_move(board: BoardEfficient, turn: Player, player: UsablePlayer, pos: int) -> tuple[BoardEfficient, Player, GameStatus]:
        if player != turn:
            raise InvalidMoveException(f"Now is {turn} turn")
            
        if TicTacToeEngineEfficient.get_game_status(board) != GameStatus.KEEP_PLAYING:
            raise GameOverException("Game is already over")
            
        if not (0 <= pos < 9):
            raise InvalidMoveException(f"Invalid position ({pos})")
            
        if board.mask_x[pos] or board.mask_o[pos]:
            raise OccupiedCellException(pos)

        if player == Player.X:
            board.mask_x[pos] = True
        else:
            board.mask_o[pos] = True
        game_status = TicTacToeEngineEfficient.get_game_status(board)
        
        if game_status == GameStatus.KEEP_PLAYING:
            new_turn = Player.O if player == Player.X else Player.X
        else:
            new_turn = Player.NONE
            
        return board, new_turn, game_status
    
    @staticmethod
    def get_current_player(board: BoardEfficient) -> Player:
        status = TicTacToeEngineEfficient.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return Player.NONE
        
        x_count = sum(board.mask_x)
        o_count = sum(board.mask_o)
        count = x_count + o_count
        return Player.X if count % 2 == 0 else Player.O

    @staticmethod
    def get_possible_moves(board: BoardEfficient) -> list[int]:
        status = TicTacToeEngineEfficient.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return []
            
        moves = []
        for i in range(9):
            if not board.mask_x[i] and not board.mask_o[i]:
                moves.append(i)
        return moves
