import ChessPieces
class ChessGame:
    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

    def move_piece(self, move):
        pieceType = move[1]
        if pieceType == "R":
            return checkRook(move, self.board)
        elif pieceType == "N":
            return checkKnight(move, self.board)
        elif pieceType == "B":
            return checkBishop(move, self.board)
        elif pieceType == "Q":
            return checkQueen(move, self.board)
        elif pieceType == "K":
            return checkKing(move, self.board)
        elif pieceType == "P":
            return checkPawn(move, self.board)
        return false

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()


def convert_l(symbol):
    return ord(symbol) - 97


def convert_n(num):
    return 8-num


c = ChessGame()
