import chess, random
import numpy as np

CHECKMATE = 10000
next_move = None


def convert(location):
    y = ord(location[0]) - 97
    x = 8 - int(location[1])
    return [x, y]


class AI:
    MATERIAL = {"P": 10.0, "R": 50.0, "Q": 100.0, "K": 10000, "N": 27.5, "B": 30.0}
    piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

    knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                     [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                     [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                     [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                     [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                     [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                     [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                     [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

    bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                     [0.0, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.0],
                     [0.0, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.0],
                     [0.2, 0.5, 0.5, 0.8, 0.8, 0.5, 0.5, 0.2],
                     [0.2, 0.4, 0.6, 0.9, 0.9, 0.6, 0.4, 0.2],
                     [0.1, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                     [0.1, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                     [0.0, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.0]]

    rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                   [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                   [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                   [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                   [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                   [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                   [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                   [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

    queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                    [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                    [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                    [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                    [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                    [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

    pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                   [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                   [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                   [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                   [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                   [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                   [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                   [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

    def __init__(self, game):
        self.game = game

    def move(self):
        moves = self.generate_moves()
        depth = 2
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
        moves = self.game.legal_moves
        temp = []
        for move in moves:
            temp.append(move)
        random.shuffle(temp)
        return temp

    def evaluate(self):
        return self.evaluate_material() + self.evaluate_position()

    def evaluate_material(self):
        score = 0.0
        for letter in range(97, 105):
            for num in range(1, 9):
                square = str(chr(int(letter))) + str(num)
                piece = board.piece_at(chess.parse_square(square))
                if piece is not None:
                    color = board.color_at(chess.parse_square(square))
                    mult = 1 if color else -1
                    if piece.piece_type == 1:
                        score += mult*1.0
                    elif piece.piece_type == 4:
                        score += mult*5.0
                    elif piece.piece_type == 3:
                        score += mult*3.0
                    elif piece.piece_type == 2:
                        score += mult*2.75
                    elif piece.piece_type == 5:
                        score += mult*10.00
        return score

    def evaluate_position(self):
        score = 0.0
        for letter in range(97, 105):
            for num in range(1, 9):
                square = str(chr(int(letter))) + str(num)
                piece = board.piece_at(chess.parse_square(square))
                if piece is not None:
                    color = board.color_at(chess.parse_square(square))
                    mult = 1 if color else -1
                    xy = convert(square)
                    if piece.piece_type == 1:
                        score += mult*self.pawn_scores[xy[0]][xy[1]]
                    elif piece.piece_type == 4:
                        score += mult*self.rook_scores[xy[0]][xy[1]]
                    elif piece.piece_type == 3:
                        score += mult*self.bishop_scores[xy[0]][xy[1]]
                    elif piece.piece_type == 2:
                        score += mult*self.knight_scores[xy[0]][xy[1]]
                    elif piece.piece_type == 5:
                        score += mult*self.queen_scores[xy[0]][xy[1]]
        return score

board = chess.Board()
ai = AI(board)

while True:
    print(board)
    move = input("What is your move: ")
    board.push(chess.Move.from_uci(move))
    ai.move()


