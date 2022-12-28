from ChessPieces import check_bishop, check_rook, check_knight, check_queen, check_king, check_pawn, convert, convert_n, \
    convert_s, in_bounds, axis, revert
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
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "bQ", "wN", "wK", "--", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["wP", "wP", "wP", "--", "--", "--", "--", "--"],
                               ["wR", "--", "--", "--", "wK", "--", "bP", "wR"]])
        # ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
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
        self.taken_material = np.array([])

    def move_piece(self, move):
        if not validate_move(move):
            return False
        if not self.turn == move[0]:
            return False
        pieceType = move[1]
        if pieceType == "R":
            return check_rook(move, self.board, self.pinned)
        elif pieceType == "N":
            return check_knight(move, self.board, self.pinned)
        elif pieceType == "B":
            return check_bishop(move, self.board, self.pinned)
        elif pieceType == "Q":
            return check_queen(move, self.board, self.pinned)
        elif pieceType == "K":
            return check_king(move, self.board, self.moved, self.covered)
        elif pieceType == "P":
            return check_pawn(move, self.board, self.moves, self.movedPawns, self.pinned)
        return False

    def move(self, move, dont_check=False):
        if dont_check or self.move_piece(move):
            coords = convert(move) #Make sure to mark that king or rook has moved
            self.handle_set(move)
            self.board[coords[2]][coords[3]] = move[0:2]
            self.board[coords[0]][coords[1]] = "--"
            row = 7 if move[0] == "w" else 0
            if move[1] == "K" and move[2:4] in ChessGame.KINGS.keys(): #King has moved
                self.moved[int(ChessGame.KINGS[move[2:4]])] = True
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
                s = ("w" if move[0] == "b" else "b") + "P" + st
                self.taken_material.append(s)
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
            s = ("w" if move[0] == "b" else "b") + str(p) + move[4:6]
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
            return valid_rook(coords, self.board, self.pinned)
        elif pieceType == "N":
            return valid_knight(coords, self.board, self.pinned)
        elif pieceType == "B":
            return valid_bishop(coords, self.board, self.pinned)
        elif pieceType == "Q":
            return valid_queen(coords, self.board, self.pinned)
        elif pieceType == "K":
            return valid_king(coords, self.board, self.moved, self.covered)
        elif pieceType == "P":
            return valid_pawn(coords, self.board, self.moves, self.movedPawns, self.pinned)

    def in_check(self, is_white, x=-1, y=-1):
        arr = self.black_material if not is_white else self.white_material
        knight_move = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [1, -2], [-2, 1]]
        attack_inc = -1 if is_white else 1
        if x == -1 and y == -1:
            xy = arr[1].pop()
            arr[1].add(xy)
            kx, ky = convert_n(xy[1]), convert_s(xy[0])
        else:
            kx, ky = x, y
        print(str(kx) + "" + str(ky))
        opp = "bK" if is_white else "wK"
        for move in knight_move:
            if in_bounds(kx + move[0], ky + move[1]) and self.board[kx + move[0]][ky + move[1]] == opp:
                return True
        opp = opp[0]
        piece = opp + "R"
        if axis(self.board, kx, ky, 1, 0, piece, opp) or axis(self.board, kx, ky, -1, 0, piece, opp) or axis(self.board, kx, ky, 0, 1, piece, opp) or axis(self.board, kx, ky, 0, -1, piece, opp):
            return True
        piece = opp + "B"
        if axis(self.board, kx, ky, 1, 1, piece, opp) or axis(self.board, kx, ky, -1, -1, piece, opp) or axis(self.board, kx, ky, -1, 1, piece, opp) or axis(self.board, kx, ky, 1, -1, piece, opp):
            return True
        # Check Left Pawn
        piece = opp + "P"
        if self.board[kx+attack_inc][ky+1] == piece or self.board[kx+attack_inc][ky-1] == piece:
            return True
        return False

    def check_dir(self, is_white, x=-1, y=-1):
        ans = []
        arr = self.black_material if not is_white else self.white_material
        knight_move = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [1, -2], [-2, 1]]
        attack_inc = -1 if is_white else 1
        if x == -1 and y == -1:
            xy = arr[1].pop()
            arr[1].add(xy)
            kx, ky = convert_n(xy[1]), convert_s(xy[0])
        else:
            kx, ky = x, y
        opp = "bK" if is_white else "wK"
        for move in knight_move:
            if in_bounds(kx + move[0], ky + move[1]) and self.board[kx + move[0]][ky + move[1]] == opp:
                ans.append((kx + move[0], ky + move[1]))
        opp = opp[0]
        piece = opp + "R"
        if axis(self.board, kx, ky, 1, 0, piece, opp) :
            ans.append((1,0))
        if axis(self.board, kx, ky, -1, 0, piece, opp) :
            ans.append((1, 0))
        if axis(self.board, kx, ky, 0, 1, piece, opp):
            ans.append((1, 0))
        if axis(self.board, kx, ky, 0, -1, piece, opp):
            ans.append((1,0))
        piece = opp + "B"
        if axis(self.board, kx, ky, 1, 1, piece, opp):
            ans.append((1,1))
        if axis(self.board, kx, ky, -1, -1, piece, opp):
            ans.append((-1, -1))
        if axis(self.board, kx, ky, -1, 1, piece, opp):
            ans.append((-1, 1))
        if axis(self.board, kx, ky, 1, -1, piece, opp):
            ans.append((1, -1))
        return ans

    def checkmate(self, coords):
        is_white = True if coords[0] == "w" else False
        x, y = convert_n(coords[3]), convert_s(coords[2])
        if not self.in_check(is_white):
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                    move = coords + revert(x + i, y + j)
                    if check_king(move, self.board, self.moved):
                        return False
        check_dir = self.check_dir(is_white)
        if len(check_dir) > 1:
            return True

        # Finish checking for blockers in directions
        return False

    def blocker(self, x, y, x_inc, y_inc, look):
        ans = []
        for i in range(7):
            x += x_inc
            y += y_inc
            if not in_bounds(x, y):
                return ans
            ans = ans + self.covered(x, y, look)
        return ans

    def covered(self, x, y, look):
        ans = []
        piece = look + "N"
        inc = 1 if look == "w" else -1
        kM = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [1, -2], [-2, 1]]
        for move in kM:
            if in_bounds(x+move[0], y+move[1]) and self.board[x+move[0]][y+move[1]] == piece:
                st = piece + revert(x+move[0], y+move[1])
                if not self.pinned(st):
                    ans.append(st)
        queen, rook, bishop, king, pawn = look + "Q", look + "R", look + "B", look + "K", look + "P"
        ans += (self.covered_help(x, y, 1, 0, rook, queen) + self.covered_help(x, y, -1, 0, rook, queen) +
                self.covered_help(x, y, 0, -1, rook, queen) + self.covered_help(x, y, 0, 1, rook, queen))
        ans += (self.covered_help(x, y, -1, -1, bishop, queen) + self.covered_help(x, y, 1, -1, bishop, queen) +
                self.covered_help(x, y, -1, 1, bishop, queen) + self.covered_help(x, y, 1, 1, bishop, queen))
        if self.board[x+inc][y+1] == pawn and not self.pinned(revert(x+inc, y+1)):
            ans.append(revert(x+inc, y+1))
        if self.board[x+inc][y-1] == pawn and not self.pinned(revert(x+inc, y-1)):
            ans.append(revert(x+inc, y-1))
        return ans

    def covered_help(self, x, y, x_inc, y_inc, piece1, piece2):
        ans = []
        opp = "w" if piece1[0] == "b" else "b"
        for i in range(7):
            x += x_inc
            y += y_inc
            if not in_bounds(x, y):
                return ans
            if self.board[x][y][0] == opp:
                return ans
            if self.board[x][y] == piece1:
                loc = piece1 + revert(x, y)
                if not self.pinned(loc):
                    ans.append(loc)
            if self.board[x][y] == piece2:
                loc = piece2 + revert(x, y)
                if not self.pinned(loc):
                    ans.append(loc)
        return ans

    def attacks(self, x, y, look):
        return self.board

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


# Need methods: Find possible moves for side, Handles Promotion

c = ChessGame()
c.move("wKe1f1")
c.print_board()
# c.move("wRh1g1")
# c.move("bPe7e5")
# c.move("wKe1g1")
# c.move("bKe8g8")
# c.move("wPe2e4")
# c.move("bPf7f5")
# c.print_board()
# c.print_moves()
