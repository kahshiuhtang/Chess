from ChessPieces import check_bishop, check_rook, check_knight, check_queen, check_king, check_pawn, convert, convert_n, \
    convert_s, in_bounds, axis, revert, valid_king, valid_pawn, valid_queen, valid_bishop, valid_rook, valid_knight
from ChessAI import ChessAi
import numpy as np


def validate_move(move):
    """
    Checks whether a move is valid or not
    :param move: string, move
    :return: boolean
    """
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
        """

        """
        self.board = np.array([["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                               ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["--", "--", "--", "--", "--", "--", "--", "--"],
                               ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                               ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])
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
        self.taken_material = []

    def recalculate(self):
        """
        Resets and recalculates the pieces in the black/white material arrays
        :return: void
        """
        self.black_material = np.array([set([]), set([]), set([]), set([]), set([]), set([]), set([]), set([])])
        self.white_material = np.array([set([]), set([]), set([]), set([]), set([]), set([]), set([]), set([])])
        for i in range(8):
            for j in range(8):
                if not self.board[i][j] == "--":
                    arr = self.black_material if self.board[i][j][0] == "b" else self.white_material
                    ind = ChessGame.IND[self.board[i][j][1]]
                    addr = revert(i, j)
                    arr[ind].add(addr)

    def move_piece(self, move):
        """
        Checks if a move is a valid move
        :param move: string, represents what piece is being moved and to where
        :return: boolean, whether the move has gone through or not
        """
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
            return check_king(move, self.board, self.moved, self.covered, self.pinned)
        elif pieceType == "P":
            return check_pawn(move, self.board, self.moves, self.movedPawns, self.pinned)
        return False

    def move(self, move, dont_check=False):
        """
        Moves a piece if it is a valid move, represented on the board and in other structures of ChessGame
        :param move: string, represents what piece is being moved and to where
        :dont_check: boolean, whether we need to check if the move string is valid
        :return: boolean, whether the move has gone through or not
        """
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
            if move[1] == "P" and not move[2] == move[4] and len(move) == 7 and move[6] == "e": #En Passant
                inc = -1 if move[0] == "w" else 1
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

    def unmove(self, moves=None, board=None, taken=None):
        """
        Reverts the last move that ocurred
        :param moves: list, string of moves, ordered from first to last
        :param board: ChessGame board
        :param taken: list, string pieces that have been taken, arranged from first to last
        :return: void
        """
        if moves is None and board is None and taken is None:
            moves = self.moves
            board = self.board
            taken = self.taken_material
        length = len(moves)
        self.turn = "w" if self.turn == "b" else "b"
        if length != 0:  # How to undo check for pawn, king, rook already moved?
            move = moves[length - 1]
            moves.pop(length - 1)
            strlen = len(move)
            x2, y2 = convert_n(move[5]), convert_s(move[4])
            x1, y1 = convert_n(move[3]), convert_s(move[2])
            piece = self.board[x2][y2]
            arr = self.black_material if piece[0] == "b" else self.white_material
            if move[4:6] in arr[ChessGame.IND[piece[1]]]:
                arr[ChessGame.IND[piece[1]]].remove(move[4:6])
            arr[ChessGame.IND[piece[1]]].add(move[2:4])
            if piece[1] == "P":
                row = "7" if piece[0] == "b" else "2"
                if move[3] == row:
                    index = convert_s(move[2])
                    pawns = self.movedPawns[0] if move[0] == "w" else self.movedPawns[1]
                    pawns[index] = False
            if strlen == 6:
                board[x2][y2] = "--"
                board[x1][y1] = move[0:2]
            elif move[6] == "x":
                pieced = taken[len(taken) - 1]
                taken.pop(len(taken) - 1)
                arr1 = self.black_material if pieced[0] == "b" else self.white_material
                arr1[ChessGame.IND[pieced[1]]].add(move[4:6])
                board[x2][y2] = pieced
                board[x1][y1] = move[0:2]
            else:
                pieced = ("w" if move[0] == "b" else "b") + "P"
                inc = -1 if move[0] == "b" else 1
                taken.pop(len(taken) - 1)
                board[x2 + inc][y2] = pieced
                arr1 = self.black_material if pieced[0] == "b" else self.white_material
                arr1[ChessGame.IND[pieced[1]]].add(revert(x2 + inc, y2))
                board[x1][y1] = move[0:2]
            return True
        return False

    def convert_to_move(self, x1, y1, x2, y2):
        """
        Turns a 4-tuple of coordinates into a string move
        :param x1: integer, first coordinate, x of the start
        :param y1: integer, second coordinate, y of the start
        :param x2: integer, third coordinate, x of the end square
        :param y2: integer, fourth coordinate, y of the end square
        :return: string, final move
        """
        ans = self.board[x1][y1]
        ans += revert(x1, y1) + revert(x2, y2)
        if self.board[x1][y1][1] == "P" and y2 - y1 != 0 and self.board[x2][y2] == "--":
            ans += "e"
        elif not self.board[x2][y2] == "--":
            ans += "x"
        return ans

    def generate_valid_moveset(self):
        """
        Creates a list of all valid moves in a certain gamestate
        :return list, of string moves that are valid:
        """
        iswhite = (self.turn == "w")
        pieces = self.white_material if iswhite else self.black_material
        col = self.turn
        ans = []
        piece_type = col + "P"
        for square in pieces[0]:
            ans += self.possible_moves(piece_type+square)
        piece_type = col + "K"
        for square in pieces[1]:
            ans += self.possible_moves(piece_type + square)
        piece_type = col + "N"
        for square in pieces[2]:
            ans += self.possible_moves(piece_type + square)
        piece_type = col + "Q"
        for square in pieces[3]:
            ans += self.possible_moves(piece_type + square)
        piece_type = col + "R"
        for square in pieces[4]:
            ans += self.possible_moves(piece_type + square)
        piece_type = col + "B"
        for square in pieces[5]:
            ans += self.possible_moves(piece_type + square)
        ans1 = []
        for move in ans:
            ans1.append(self.convert_to_move(move[0], move[1], move[2], move[3]))
        return ans1

    def handle_set(self, move):
        """
        Handles the material and moved sets/lists that we maintain
        :param move: string, the move we are carryign out, already checking
        :return: void
        """
        arr = self.black_material if move[0] == "b" else self.white_material
        ind = int(ChessGame.IND[move[1]])
        arr[ind].remove(move[2:4])
        arr[ind].add(move[4:6])
        if len(move) == 7 and move[6] == "x":
            arr = self.black_material if move[0] == "w" else self.white_material
            c = [convert_n(move[5]), convert_s(move[4])]
            p = str(self.board[c[0]][c[1]][1])
            if p == "K":
                return
            s = ("w" if move[0] == "b" else "b") + str(p)
            arr[ChessGame.IND[p]].remove(move[4:6])
            self.taken_material.append(s)

    def print_board(self):
        """
        Prints the chess board's current state
        :return: void
        """
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()

    def print_moves(self):
        """
        Prints out list of moves that have occurred
        :return: none
        """
        for move in self.moves:
            print(move, end="->")
        print("END")

    def possible_moves(self, coords):
        """
        Returns a list of moves for a specific piece
        :param coords: strings, represent what square we are looking at
        :return: list, strings that represent valid moves
        """
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
        """
        Returns whether the side is in check or not
        :param is_white: boolean, whether we are checking if white/black is in check or not
        :param x: integer, first index of array
        :param y: integer, second index of array
        :return: boolean, whether a side is in check or not
        """
        arr = self.black_material if not is_white else self.white_material
        knight_move = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [1, -2], [-2, 1]]
        attack_inc = -1 if is_white else 1
        if x == -1 and y == -1:
            xy = arr[1].pop()
            arr[1].add(xy)
            kx, ky = convert_n(xy[1]), convert_s(xy[0])
        else:
            kx, ky = x, y
        opp = "bN" if is_white else "wN"
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
        piece = opp + "P"
        if self.board[kx+attack_inc][ky+1] == piece or self.board[kx+attack_inc][ky-1] == piece:
            return True
        return False

    def check_dir(self, is_white, x=-1, y=-1):
        """
        Creates a list of all directions of attack on the kiing
        :param is_white: string, what color we are looking for w or b
        :param x: integer, coordinate on board
        :param y: integer, coordinate on board
        :return: list, of 4-tuples, start and end of move
        """
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
        pawn = "bP" if is_white else "wP"
        if in_bounds(kx + attack_inc, ky+1) and self.board[kx + attack_inc][ky+1] == pawn:
            ans.append((kx + attack_inc, ky+1,0))
        if in_bounds(kx + attack_inc, ky -1)and self.board[kx + attack_inc][ky-1] == pawn:
            ans.append((kx + attack_inc, ky - 1, 0))
        opp = "bN" if is_white else "wN"
        for move in knight_move:
            if in_bounds(kx + move[0], ky + move[1]) and self.board[kx + move[0]][ky + move[1]] == opp:
                ans.append((kx + move[0], ky + move[1]))
        opp = opp[0]
        piece = opp + "R"
        if axis(self.board, kx, ky, 1, 0, piece, opp) :
            ans.append((1, 0))
        if axis(self.board, kx, ky, -1, 0, piece, opp) :
            ans.append((-1, 0))
        if axis(self.board, kx, ky, 0, 1, piece, opp):
            ans.append((0, 1))
        if axis(self.board, kx, ky, 0, -1, piece, opp):
            ans.append((0, -1))
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

    def same_axis(self, x, y, dirs):
        """
        Used for looking at whether a piece is in between an attack on the king
        :param x: integer, coordinate
        :param y: integer, coordinate
        :param dirs: 2-tuple of integers, represents direction
        :return: boolean, whether piece is aligned in attack
        """
        for dir in dirs:
            if abs(dir[0]) < 2 and abs(dir[1]) < 2 and len(dir) == 2:
                if x == dir[1] and y != dir[0] or x == dir[0] and y != dir[1]:
                    return True
        return False

    def checkmate(self, coords):
        """
        Returns whether a side has been checkmated
        :param coords: string, coordinates of the king
        :return: boolean, whether side is checkmated or not
        """
        is_white = True if coords[0] == "w" else False
        x, y = convert_n(coords[3]), convert_s(coords[2])
        check_dir = self.check_dir(is_white)
        if not self.in_check(is_white):
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self.same_axis(i, j, check_dir):
                    move = coords + revert(x + i, y + j)
                    if check_king(move, self.board, self.moved, self.covered, self.pinned):
                        return False
        if len(check_dir) > 1:
            return True
        if len(check_dir) == 0:
            return False
        xinc, yinc = check_dir[0][0], check_dir[0][1]
        col = coords[0]
        temp = self.blocker(x, y, xinc, yinc, col)
        return len(temp) == 0

    def blocker(self, x, y, x_inc, y_inc, look):
        """
        Looks in a direction and sees if there is a valid move that blocks an attack
        :param x: integer, location of where we are checking on board
        :param y: integer, location of where we are checking on board
        :param x_inc: integer, increment, helps indicate direction of attacl
        :param y_inc: integer, increment, helps indicate direction of attack
        :param look: string, whether piece is white or black
        :return: list of moves, moves can block
        """
        ans = []
        for i in range(7):
            x += x_inc
            y += y_inc
            if not in_bounds(x, y) or (not self.board[x][y] == "--" and not self.board[x][y][0] == look):
                return ans
            ans = ans + self.covered(x, y, look)
        return ans

    def covered(self, x, y, look):
        """
        Finds a list of string moves
        :param x: integer, x coordinate on board
        :param y: integer, y coordinate on board
        :param look: string, is either w or b depending on what colored piece we are looking for
        :return: list, of string moves that would block the attack
        """
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
        if in_bounds(x+inc, y+1) and self.board[x+inc][y+1] == pawn and not self.pinned(look + "P" + revert(x+inc, y+1)):
            ans.append(revert(x+inc, y+1))
        if in_bounds(x+inc, y-1) and self.board[x+inc][y-1] == pawn and not self.pinned(look + "P" + revert(x+inc, y-1)):
            ans.append(revert(x+inc, y-1))
        return ans

    def covered_help(self, x, y, x_inc, y_inc, piece1, piece2):
        """
        Returns a list of pieces + coordinates that would be able to move in to cover the square
        :param x: integer, first coordinate on board
        :param y: integer, second coordinate on board
        :param x_inc: integer, increment direction
        :param y_inc: integer, increment direction
        :param piece1: string, piece we are looking for
        :param piece2: string, second piece we are looking for
        :return: list, of string pieces + location
        """
        ans = []
        for i in range(7):
            x += x_inc
            y += y_inc
            if not in_bounds(x, y):
                return ans
            if not self.board[x][y] == "--" and not self.board[x][y] == piece1 and not self.board[x][y] == piece2:
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

    def pinned(self, coords):
        """
        Returns whether a piece is pinned
        :param coords: string, coordinates of where
        :return: boolean, whether piece is pinned
        """
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
ai = ChessAi(c)
"""
Game Loop
"""
while True:
    c.print_board()
    move = input("Enter move:")
    c.move(move)
    ai.move_turn()


