from app.core.constants import Player, GameStatus
from app.core.types import UsablePlayer, BoardType


class TicTacToeEngine:
    """TicTacToe Engine. Always starts X."""

    @staticmethod
    def init_board() -> tuple[BoardType, Player, GameStatus]:
        board = [
            [
                Player.NONE 
                for _ in range(3)
            ]
            for _ in range(3)
        ]
        return board, Player.X, GameStatus.KEEP_PLAYING
    
    @staticmethod
    def get_game_status(board: BoardType) -> GameStatus:
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != Player.NONE:
                return GameStatus.WIN_X if board[i][0] == Player.X else GameStatus.WIN_O
            if board[0][i] == board[1][i] == board[2][i] != Player.NONE:
                return GameStatus.WIN_X if board[0][i] == Player.X else GameStatus.WIN_O

        if board[0][0] == board[1][1] == board[2][2] != Player.NONE:
            return GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O
        if board[0][2] == board[1][1] == board[2][0] != Player.NONE:
            return GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O

        if any(Player.NONE in row for row in board):
            return GameStatus.KEEP_PLAYING

        return GameStatus.DRAW
    
    @staticmethod
    def validate_board(board: BoardType, turn: Player):
        status = TicTacToeEngine.get_game_status(board)
        
        x_count = sum(row.count(Player.X) for row in board)
        o_count = sum(row.count(Player.O) for row in board)
        
        if not (o_count + 1 >= x_count >= o_count):
            raise ValueError("Invalid board: turn count imbalance.")
        if x_count == o_count and turn != Player.X:
            raise ValueError("Invalid board: turn must be X.")
        if x_count > o_count and turn != Player.O:
            raise ValueError("Invalid board: turn must be O.")

        if status != GameStatus.KEEP_PLAYING:
            turn = Player.NONE
        elif turn == Player.NONE:
            raise ValueError("Game is ongoing; turn must be X or O.")
    
    @staticmethod
    def make_move(board: BoardType, turn: Player, player: UsablePlayer, row: int, col: int) -> tuple[BoardType, Player, GameStatus]:
        if player != turn:
            raise ValueError(f"Now is {turn} turn")
            
        if TicTacToeEngine.get_game_status(board) != GameStatus.KEEP_PLAYING:
            raise ValueError("Game is already over")
            
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError(f"Invalid coordinates ({row}, {col})")
            
        if board[row][col] != Player.NONE:
            raise ValueError(f"Occupied cell ({row}, {col})")

        board[row][col] = player
        game_status = TicTacToeEngine.get_game_status(board)
        
        if game_status == GameStatus.KEEP_PLAYING:
            new_turn = Player.O if player == Player.X else Player.X
        else:
            new_turn = Player.NONE
            
        return board, new_turn, game_status
    
    @staticmethod
    def get_current_player(board: BoardType) -> Player:
        status = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return Player.NONE
        
        x_count = sum(row.count(Player.X) for row in board)
        o_count = sum(row.count(Player.O) for row in board)
        count = x_count + o_count
        return Player.X if count % 2 == 0 else Player.O
