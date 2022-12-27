from ChessPieces import check_bishop, check_rook, check_knight, check_queen, check_king, check_pawn, convert, convert_n, \
    convert_s, in_bounds
import numpy as np


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
    """Representation of a Chess Board"""
    PIECES = {"P", "K", "N", "Q", "R", "B"}
    CORNERS = {"h1": 0, "h8": 1, "a1": 2, "a8": 3}
    KINGS = {"e1": 4, "e8": 5}
    IND = {"P": 0, "K": 1, "N": 2, "Q": 3, "R": 4, "B": 5}

    def __init__(self):
        self.board = np.array([["bR", "bN", "bB", "bQ", "bK", "--", "--", "bR"],
                               ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                               ["--", "--", "--", "--", "wR", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "bQ", "wN", "wK", "bQ", "bP", "--", "--"],
                               ["--", "--", "--", "--", "wP", "--", "bR", "--"],
                               ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                               ["wR", "--", "--", "--", "wK", "--", "bP", "wR"]])
        # ["wR", "wN", "wB", "wQ", "wK", "--", "wN", "wR"]
        # ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
        self.moved = [False, False, False, False, False, False] #uL -> uR -> bL -> bR -> wK -> bK of rooks
        self.turn = "w"
        self.movedPawns = [[False, False, False, False, False, False, False, False],
                           [False, False, False, False, False, False, False, False]]
        self.moves = []
        self.black_material = np.array([{"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"}, {"e8"},
                                        {"b8", "g8"}, {"d8"}, {"a8", "h8"}, {"c8", "f8"}])
        self.white_material = np.array([{"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"}, {"e1"}, {"b1", "g1"}, {"d1"},
                                        {"a1", "h1"}, {"c1", "f1"}])

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
            return check_pawn(move, self.board, self.moves, self.movedPawns)
        return False

    def move(self, move):
        if self.move_piece(move):
            coords = convert(move) #Make sure to mark that king or rook has moved
            self.handle_set(move)
            self.board[coords[2]][coords[3]] = move[0:2]
            self.board[coords[0]][coords[1]] = "--"
            row = 7 if move[0] == "w" else 0
            if move[1] == "K" and move[2:4] in ChessGame.KINGS.keys(): #King has moved
                self.moved[int(ChessGame.CORNERS[move[2:4]])] = True
            if move[1] == "R" and move[2:4] in ChessGame.CORNERS.keys(): #Rook has moved
                self.moved[int(ChessGame.CORNERS[move[2:4]])] = True
            if move[1] == "P" and (move[3] == "7" or move[3] == "2"): #Pawn has moved
                row = 0 if move[0] == "w" else 1
                self.movedPawns[row][coords[1]] = True
            if move[1] == "P" and not move[2] == move[4]: #En Passant
                inc = 1 if move[0] == "w" else -1
                self.board[coords[2]+inc][coords[3]] = "--"
                st = move[4] + str(int(move[5]) + inc)
                arr = self.black_material if move[0] == "w" else self.white_material
                arr[0].remove(st)
            if move[1] == "K" and abs(coords[1] - coords[3]) == 2 and abs(coords[0] - coords[2]) == 0 and move[4] == "g": #Castle Kingside
                self.board[row][5] = move[0]+"R"
                self.board[row][7] = "--"
                arr = self.black_material if move[0] == "b" else self.white_material
                coords1 = "h8" if move[0] == "b" else "h1"
                coords2 = "f8" if move[0] == "b" else "f1"
                arr[4].remove(coords1)
                arr[4].add(coords2)
            elif move[1] == "K" and abs(coords[1] - coords[3]) == 2 and abs(coords[0] - coords[2]) == 0: #Castle Queenside
                self.board[row][3] = move[0]+"R"
                self.board[row][0] = "--"
                arr = self.black_material if move[0] == "b" else self.white_material
                coords1 = "a8" if move[0] == "b" else "a1"
                coords2 = "d8" if move[0] == "b" else "d1"
                arr[4].remove(coords1)
                arr[4].add(coords2)
            self.turn = "w" if self.turn == "b" else "b"
            self.moves.append(move)
            return True
        return False

    def handle_set(self, move):
        arr = self.black_material if move[0] == "b" else self.white_material
        ind = int(ChessGame.IND[move[1]])
        arr[ind].remove(move[2:4])
        arr[ind].add(move[4:6])
        if len(move) == 7 and move[6] == "x":
            arr = self.black_material if move[0] == "w" else self.white_material
            c = [convert_s(move[5]), convert_n(move[4])]
            p = board[c[0]][c[1]][1]
            arr[p].remove(move[4:6])

    def print_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def print_moves(self):
        for move in self.moves:
            print(move, end="->")
        print("END")

    def possible_moves(self, coords):
        pieceType = coords[1]
        if pieceType == "R":
            return valid_rook(coords, self.board)
        elif pieceType == "N":
            return valid_knight(coords, self.board)
        elif pieceType == "B":
            return valid_bishop(coords, self.board)
        elif pieceType == "Q":
            return valid_queen(coords, self.board)
        elif pieceType == "K":
            return valid_king(coords, self.board, self.moved)
        elif pieceType == "P":
            return valid_pawn(coords, self.board, self.moves, self.movedPawns)

    def squares_covered(self):
        return []

    def in_check(self):
        return []

    def check_mate(self):
        return False

    def pinned(self, coords):
        arr = self.black_material if coords[0] == "b" else self.white_material
        is_white = coords[0]
        addr = arr[1].pop()
        arr[1].add(addr)
        x, y = convert_n(coords[3]), convert_s(coords[2])
        kx, ky = convert_n(addr[1]), convert_s(addr[0])
        if (x-kx == 0 or y-ky == 0) or abs(x-kx) == abs(y-ky): #Aligned on diagonal, row or column
            incX = 0 if x - kx == 0 else -1 if kx - x > 0 else 1
            incY = 0 if y - ky == 0 else -1 if ky - y > 0 else 1
            comp = "B" if incX != 0 and incY != 0 else "R"
            for i in range(8):
                x += incX
                y += incY
                if not in_bounds(x, y) or (self.board[x][y][0] == is_white):
                    return False
                if not self.board[x][y] == "--" and not self.board[x][y][0] == is_white and (self.board[x][y][1] == "Q"
                                                                                             or self.board[x][y][1] ==
                                                                                             comp):
                    return True
        return False


c = ChessGame()
print(c.pinned("bPe7"))
#c.move("wRh1g1")
#c.move("bPe7e5")
#c.move("wKe1g1")
#c.move("bKe8g8")
#c.move("wPe2e4")
#c.move("bPf7f5")
#c.print_board()
#c.print_moves()
