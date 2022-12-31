import chess, random
import numpy as np

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

    queen_scores = [[1.0, 1.2, 1.3, 1.4, 1.4, 1.3, 1.2, 1.0],
                    [0.65, 0.75, 0.85, 0.95, 0.95, 0.85, 0.75, 0.65],
                    [0.80, 0.90, 1.00, 1.25, 1.25, 1.00, 0.90, 0.80],
                    [0.70, 0.90, 1.00, 1.50, 1.50, 1.00, 0.90, 0.70],
                    [0.65, 0.75, 0.85, 1.00, 1.00, 0.85, 0.75, 0.65],
                    [0.20, 0.30, 0.50, 0.75, 0.75, 0.50, 0.40, 0.20],
                    [0.10, 0.30, 0.35, 0.50, 0.50, 0.35, 0.30, 0.10],
                    [0.00, 0.20, 0.20, 0.30, 0.30, 0.20, 0.20, 0.00]]

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
        self.minmax(moves, depth, depth, -CHECKMATE, CHECKMATE, 1 if self.game.turn else -1)
        global next_move
        self.game.push(next_move)

    def minmax(self, valid_moves, depth, DEPTH,  alpha, beta, tm):
        """
        MinMax algorithm
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
                        score += mult * self.rook_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 3:
                        score += mult*3.0
                        score += mult * self.bishop_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 2:
                        score += mult*2.75
                        score += mult * self.knight_scores[::mult][xy[0]][xy[1]]
                    elif piece.piece_type == 5:
                        score += mult*10.00
                        score += mult * self.queen_scores[::mult][xy[0]][xy[1]]
        return score


board = chess.Board()
ai = AI(board)
sum = 0.0
for i in range(25):
    board = chess.Board()
    ai = AI(board)
    board.push(chess.Move.from_uci("e2e4"))
    ai.move()
    sum += count
print(sum/25)

while True:
    print(board)
    print(count)
    move = input("What is your move: ")
    if move == "quit":
        break
    board.push(chess.Move.from_uci(move))
    ai.move()


