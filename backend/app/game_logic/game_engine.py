from app.core.constants import Player, GameStatus, UsablePlayer, BoardType
from app.core.exceptions import InvalidMoveException, OccupiedCellException, GameOverException


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
    def get_game_status(board: BoardType) -> tuple[GameStatus, list[tuple[int, int]]]:
        # Rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != Player.NONE:
                status = GameStatus.WIN_X if board[i][0] == Player.X else GameStatus.WIN_O
                return status, [(i, 0), (i, 1), (i, 2)]
        
        # Cols
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] != Player.NONE:
                status = GameStatus.WIN_X if board[0][i] == Player.X else GameStatus.WIN_O
                return status, [(0, i), (1, i), (2, i)]

        # Diagonals
        if board[0][0] == board[1][1] == board[2][2] != Player.NONE:
            status = GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O
            return status, [(0, 0), (1, 1), (2, 2)]
            
        if board[0][2] == board[1][1] == board[2][0] != Player.NONE:
            status = GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O
            return status, [(0, 2), (1, 1), (2, 0)]

        if any(Player.NONE in row for row in board):
            return GameStatus.KEEP_PLAYING, []

        return GameStatus.DRAW, []
    
    @staticmethod
    def validate_board(board: BoardType, turn: Player):
        status, _ = TicTacToeEngine.get_game_status(board)
        
        x_count = sum(row.count(Player.X) for row in board)
        o_count = sum(row.count(Player.O) for row in board)
        
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
    def make_move(board: BoardType, turn: Player, player: UsablePlayer, row: int, col: int) -> tuple[BoardType, Player, GameStatus]:
        if player != turn:
            raise InvalidMoveException(f"Now is {turn} turn")
            
        status, _ = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            raise GameOverException("Game is already over")
            
        if not (0 <= row < 3 and 0 <= col < 3):
            raise InvalidMoveException(f"Invalid coordinates ({row}, {col})")
            
        if board[row][col] != Player.NONE:
            raise OccupiedCellException((row, col))

        board[row][col] = player
        game_status, win_line = TicTacToeEngine.get_game_status(board)
        
        if game_status == GameStatus.KEEP_PLAYING:
            new_turn = Player.O if player == Player.X else Player.X
        else:
            new_turn = Player.NONE
            
        return board, new_turn, game_status, win_line
    
    @staticmethod
    def get_current_player(board: BoardType) -> Player:
        status, _ = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return Player.NONE
        
        x_count = sum(row.count(Player.X) for row in board)
        o_count = sum(row.count(Player.O) for row in board)
        count = x_count + o_count
        return Player.X if count % 2 == 0 else Player.O

    @staticmethod
    def get_possible_moves(board: BoardType) -> list[tuple[int, int]]:
        status, _ = TicTacToeEngine.get_game_status(board)
        if status != GameStatus.KEEP_PLAYING:
            return []
            
        moves = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == Player.NONE:
                    moves.append((r, c))
        return moves
