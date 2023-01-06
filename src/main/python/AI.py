import chess, random
import numpy as np
import psycopg

CHECKMATE = 100
next_move = None
count = 0

def convert(location):
    """
    :param location: string, length 2, a corodinate on the chess board
    :return: list, length 2, first index is the x coordinate of the chess board and second index os y coordinate
    """
    y = ord(location[0]) - 97
    x = 8 - int(location[1])
    return [x, y]

def convert_s(symbol):
    return ord(symbol) - 97


def convert_n(num):
    return 8-int(num)


def revert(x, y):
    """
    Turns two integers into a string coordinate
    :param x:
    :param y:
    :return: string
    """
    fir = chr(ord('a') + y)
    sec = 8 - int(x)
    return str(fir) + str(sec)


class AI:
    """
    Chess AI that uses minmax algorithm to calculate next move
    Positional scores of pieces are stored in following 2D arrays
    """
    knight_scores = [[0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
                     [0.15, 0.20, 0.20, 0.25, 0.25, 0.20, 0.20, 0.15],
                     [0.20, 0.35, 0.45, 0.45, 0.45, 0.45, 0.35, 0.20],
                     [0.20, 0.25, 0.45, 0.55, 0.55, 0.45, 0.25, 0.20],
                     [0.15, 0.20, 0.45, 0.50, 0.50, 0.45, 0.20, 0.15],
                     [0.10, 0.20, 0.30, 0.35, 0.35, 0.30, 0.30, 0.10],
                     [0.10, 0.10, 0.20, 0.25, 0.25, 0.20, 0.10, 0.10],
                     [0.00, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.00]]

    bishop_scores = [[0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
                     [0.00, 0.15, 0.25, 0.35, 0.35, 0.25, 0.15, 0.00],
                     [0.10, 0.25, 0.35, 0.45, 0.45, 0.35, 0.25, 0.10],
                     [0.10, 0.25, 0.35, 0.65, 0.65, 0.35, 0.25, 0.10],
                     [0.15, 0.30, 0.40, 0.75, 0.75, 0.40, 0.30, 0.15],
                     [0.25, 0.30, 0.40, 0.65, 0.65, 0.40, 0.30, 0.25],
                     [0.40, 0.60, 0.50, 0.50, 0.50, 0.50, 0.60, 0.40],
                     [0.50, 0.35, 0.25, 0.30, 0.30, 0.25, 0.35, 0.60]]

    rook_scores = [[0.70, 0.95, 1.05, 1.25, 1.25, 1.05, 0.95, 0.70],
                   [0.55, 0.65, 0.75, 0.85, 0.85, 0.75, 0.65, 0.55],
                   [0.35, 0.45, 0.55, 0.65, 0.65, 0.55, 0.45, 0.35],
                   [0.30, 0.40, 0.45, 0.55, 0.55, 0.45, 0.40, 0.30],
                   [0.25, 0.35, 0.45, 0.60, 0.60, 0.45, 0.35, 0.25],
                   [0.20, 0.30, 0.35, 0.55, 0.55, 0.35, 0.30, 0.20],
                   [0.10, 0.15, 0.20, 0.50, 0.50, 0.25, 0.25, 0.10],
                   [0.15, 0.25, 0.35, 0.45, 0.45, 0.35, 0.25, 0.15]]

    queen_scores = [[0.25, 0.30, 0.30, 0.35, 0.35, 0.30, 0.30, 0.25],
                    [0.20, 0.25, 0.25, 0.35, 0.35, 0.25, 0.25, 0.20],
                    [0.15, 0.10, 0.20, 0.25, 0.25, 0.20, 0.10, 0.15],
                    [0.20, 0.25, 0.25, 0.35, 0.35, 0.25, 0.25, 0.20],
                    [0.15, 0.25, 0.30, 0.40, 0.40, 0.30, 0.25, 0.15],
                    [0.10, 0.15, 0.25, 0.30, 0.30, 0.25, 0.15, 0.10],
                    [0.05, 0.10, 0.15, 0.25, 0.25, 0.15, 0.10, 0.05],
                    [0.00, 0.10, 0.10, 0.20, 0.20, 0.10, 0.10, 0.00]]

    pawn_scores = [[1.00, 1.20, 1.40, 1.50, 1.50, 1.40, 1.20, 1.00],
                   [0.70, 0.75, 0.85, 0.95, 0.95, 0.85, 0.75, 0.70],
                   [0.50, 0.60, 0.65, 0.75, 0.75, 0.65, 0.60, 0.50],
                   [0.35, 0.45, 0.55, 0.65, 0.65, 0.55, 0.45, 0.35],
                   [0.25, 0.45, 0.45, 0.50, 0.50, 0.45, 0.45, 0.25],
                   [0.10, 0.20, 0.25, 0.30, 0.30, 0.25, 0.20, 0.10],
                   [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
                   [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]]

    def __init__(self, game):
        self.game = game

    def move(self):
        """
        Calls the minmax algorithm
        Will have the best move stored in a global variable called next_move
        :return: void
        """
        moves = self.generate_moves()
        depth = 3
        global count
        count = 0
        global next_move
        self.minmax(moves, depth, depth, -CHECKMATE, CHECKMATE, 1 if self.game.turn else -1)
        with psycopg.connect("dbname=test user=postgres") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT  INTO test (id, move) VALUES (%s, %s) on conflict(id) do update set move = (%s)",
                    (board.fen(), next_move.uci(), next_move.uci()))
                cur.execute("SELECT * FROM test")
                cur.fetchone()
                for record in cur:
                    print(record)
        self.game.push(next_move)

    def minmax(self, valid_moves, depth, DEPTH,  alpha, beta, tm):
        """
        MinMax algorithm with alpha-beta pruning
        Recursively finds the best move based on after each possible move up to certain depth
        :param valid_moves: string list, valid moves at a specific position
        :param depth: integer, how close we are until the function returns
        :param DEPTH: integer, depth we are iterating until
        :param alpha: integer,
        :param beta: integer, along with alpha, use to prune down branches that will never lead to better outcomes
        :param tm: integer, -1 or 1, what to multiply position score by depending on whose turn it is
        :return: float, score evaluation of position
        """
        if depth == 0:
            return tm * self.evaluate()
        # move ordering - implement later //TODO
        max_score = -CHECKMATE
        for move in valid_moves:
            self.game.push(move)
            next_moves = self.generate_moves()
            score = -self.minmax(next_moves, depth - 1, DEPTH, -beta, -alpha, -tm)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    global next_move
                    next_move = move
            self.game.pop()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    def generate_moves(self):
        """
        Converts a generator into a list for sorting
        :return: list, list of moves that are valid
        """
        global count
        count = count + 1
        moves = self.game.legal_moves
        temp = []
        for move in moves:
            temp.append(move)
        random.shuffle(temp)
        return temp

    def evaluate(self):
        """
        Evaluates the score of this position
        Score > 0 is better for white and score < 0 is better for black
        :return: float, score of this position
        """
        return self.evaluate_material_and_positioning()

    def evaluate_material_and_positioning(self):
        score = 0.0
        if self.game.is_checkmate():
            mult = 1 if self.game.turn else -1
            return mult*CHECKMATE
        if self.game.is_stalemate():
            return score
        for letter in range(97, 105):
            for num in range(1, 9):
                square = str(chr(int(letter))) + str(num)
                piece = board.piece_at(chess.parse_square(square))
                if piece is not None:
                    color = board.color_at(chess.parse_square(square))
                    mult = 1 if color else -1
                    xy = convert(square)
                    if piece.piece_type == 1:
                        score += mult*1.0
                        score += mult * self.pawn_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 4:
                        score += mult*5.0
                        score += mult*self.rook_attacker_score(square, color)
                        score += mult * self.rook_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 3:
                        score += mult*3.0
                        score += mult * self.bishop_attacker_score(square, color)
                        score += mult * self.bishop_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 2:
                        score += mult*2.75
                        score += mult * self.knight_attacker_score(square, color)
                        score += mult * self.knight_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 5:
                        score += mult*10.00
                        score += mult * self.queen_attacker_score(square, color)
                        score += mult * self.queen_scores[::mult][xy[0]][xy[1]]
        return score

    def rook_attacker_score(self, coords, color):
        """
            :param coords: string, coordinates of piece we are checking
            :return: double - score of the attacking strength of this piece
            """
        if self.game.is_pinned(color, chess.parse_square(coords)):
            return -3.0
        return self.check_direction(coords, color, 1, 0) + self.check_direction(coords, color, 0, 1) + \
               self.check_direction(coords, color, -1, 0) + self.check_direction(coords, color, 0, -1)

    def bishop_attacker_score(self, coords, color):
        """
            :param coords: string, coordinates of piece we are checking
            :return: double - score of the attacking strength of this piece
        """
        if self.game.is_pinned(color, chess.parse_square(coords)):
            return -1.5
        return self.check_direction(coords, color, 1, 1) + self.check_direction(coords, color, -1, 1) + \
               self.check_direction(coords, color, -1, -1) + self.check_direction(coords, color, 1, -1)

    def queen_attacker_score(self, coords, color):
        """
            :param coords: string, coordinates of piece we are checking
            :return: double - score of the attacking strength of this piece
        """
        if self.game.is_pinned(color, chess.parse_square(coords)):
            return -7.0
        return self.rook_attacker_score(coords, color) + self.bishop_attacker_score(coords, color)

    def knight_attacker_score(self, coords, color):
        """
            :param coords: string, coordinates of piece we are checking
            :return: double - score of the attacking strength of this piece
        """
        if self.game.is_pinned(color, chess.parse_square(coords)):
            return -1.25
        moves = [[1, 2], [2, 1], [-1, 2], [2, -1], [-1, -2], [-2, -1], [1, -2], [-2, 1]]
        orig = board.piece_at(chess.parse_square(coords))
        x = convert_s(coords[0])
        y = convert_n(coords[1])
        ans = 0
        for move in moves:
            if x + move[0] < 0 or x + move[0] > 7 or y + move[1] < 0 or y + move[1] > 7:
                pass
            else:
                strn = revert(x + move[0], y + move[1])
                piece = board.piece_at(chess.parse_square(strn))
                if piece is not None:
                    is_white = board.color_at(chess.parse_square(strn))
                    if color == is_white:
                        if piece.piece_type == 1:
                            ans += 0.15 if orig.piece_type - piece.piece_type > 0 else 0.25
                        elif piece.piece_type == 2:
                            ans += 0.4 if orig.piece_type - piece.piece_type > 0 else 0.75
                        elif piece.piece_type == 3:
                            ans += 0.5 if orig.piece_type - piece.piece_type > 0 else 0.9
                        elif piece.piece_type == 4:
                            ans += 0.75 if orig.piece_type - piece.piece_type > 0 else 1.25
                        elif piece.piece_type == 5:
                            ans += 1 if orig.piece_type - piece.piece_type > 0 else 3
        return ans

    def check_direction(self, coords, is_white, x_inc, y_inc):
        """
        :param coords: string, coordinates of starting square
        :param is_white: boolean, whether we are looking for white or black pieces
        :param x_inc: int, how much x index increases
        :param y_inc: int, how much y index increase
        :return: double: score of how valuable this piece it is attacking is
        """
        orig = board.piece_at(chess.parse_square(coords))
        x = convert_s(coords[0])
        y = convert_n(coords[1])
        for i in range(8):
            x += x_inc
            y += y_inc
            if x < 0 or x > 7 or y < 0 or y > 7:
                return 0
            square = revert(x, y)
            piece = board.piece_at(chess.parse_square(square))
            if piece is not None:
                color = board.color_at(chess.parse_square(square))
                if color == is_white:
                    if piece.piece_type == 1:
                        return 0.15 if orig.piece_type - piece.piece_type > 0 else 0.25
                    elif piece.piece_type == 2:
                        return 0.4 if orig.piece_type - piece.piece_type > 0 else 0.75
                    elif piece.piece_type == 3:
                        return 0.5 if orig.piece_type - piece.piece_type > 0 else 0.9
                    elif piece.piece_type == 4:
                        return 0.75 if orig.piece_type - piece.piece_type > 0 else 1.25
                    elif piece.piece_type == 5:
                        return 1 if orig.piece_type - piece.piece_type > 0 else 3
                else:
                    return 0


with psycopg.connect("dbname=test user=postgres") as conn:
    with conn.cursor() as cur:
        print("Here")
        #cur.execute("""CREATE TABLE test (id text PRIMARY KEY,move text)""")
board = chess.Board()
print(board.fen())
ai = AI(board)
#sum = 0.0
#for i in range(5):
#    board = chess.Board()
#    ai = AI(board)
#    board.push(chess.Move.from_uci("e2e4"))
#    ai.move()
#    sum += count
#print(sum/5)

while True:
    print(board)
    print(count)
    move = input("What is your move: ")
    if move == "quit":
        break
    board.push(chess.Move.from_uci(move))
    ai.move()


