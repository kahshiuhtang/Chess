from ChessPieces import check_bishop, check_rook, check_knight, check_queen, check_king, check_pawn, convert


def validate_move(move):
    if len(move) < 6 or len(move) > 7:
        return False
    if not (move[0] == 'w' or move[0] == 'b'):
        return False
    if not move[1] in ChessGame.PIECES:
        return False
    coords = convert(move)
    for i in coords:
        if i < 0 or i > 7:
            return False
    return True


class ChessGame:
    PIECES = {"P", "K", "N", "Q", "R", "B"}
    CORNERS = {"h1": 0, "h8": 1, "a1": 2, "a8": 3}

    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "--", "--", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]
        # ["wR", "wN", "wB", "wQ", "wK", "--", "wN", "wR"]
        # ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        self.moved = [False, False, False, False, False, False] #uL -> uR -> bL -> bR -> wK -> bK of rooks
        self.turn = "w"
        self.movedPawnsB = [False, False, False, False, False, False, False, False]
        self.movedPawnsW = [False, False, False, False, False, False, False, False]
        self.moves = []

    def move_piece(self, move):
        if not validate_move(move):
            return False
        if not self.turn == move[0]:
            return False
        pieceType = move[1]
        if pieceType == "R":
            return check_rook(move, self.board)
        elif pieceType == "N":
            return check_knight(move, self.board)
        elif pieceType == "B":
            return check_bishop(move, self.board)
        elif pieceType == "Q":
            return check_queen(move, self.board)
        elif pieceType == "K":
            return check_king(move, self.board, self.moved)
        elif pieceType == "P":
            return check_pawn(move, self.board, self.moves)
        return False

    def move(self, move):
        if self.move_piece(move):
            coords = convert(move) #Make sure to mark that king or rook has moved
            self.board[coords[2]][coords[3]] = move[0:2]
            self.board[coords[0]][coords[1]] = "--"
            row = 7 if move[0] == "w" else 0
            if move[1] == "R" and move[2:4] in ChessGame.CORNERS.keys():
                self.moved[int(ChessGame.CORNERS[move[2:4]])] = True
                print(self.moved)
            if move[1] == "K" and abs(coords[1] - coords[3]) == 2 and abs(coords[0] - coords[2]) == 0 and move[4] == "g":
                self.board[row][5] = move[0]+"R"
                self.board[row][7] = "--"
            elif move[1] == "K" and abs(coords[1] - coords[3]) == 2 and abs(coords[0] - coords[2]) == 0:
                self.board[row][3] = move[0]+"R"
                self.board[row][0] = "--"
            self.turn = "w" if self.turn == "b" else "b"
            self.moves.append(move)
            return True
        return False

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def print_moves(self):
        for move in self.moves:
            print(move)


c = ChessGame()
c.move("wRa8a7")
c.move("bPe7e5")
c.move("wKe1g1")
c.move("bKe8g8")
c.print_board()
c.print_moves()
