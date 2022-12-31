import random
import numpy as np
next_move = None
count = 0
CHECKMATE = 100000


class ChessAi:
    MATERIAL = {"P": 10.0, "R": 50.0, "Q": 100.0, "K": 10000, "N": 27.5, "B": 30.0}
    DEPTH = 2
    KNIGHT_POS = np.array([[1, 3, 5, 5, 5, 5, 3, 1],
                           [1, 3.5, 4, 5, 5, 4, 3.5, 1],
                           [1, 3, 8, 7, 7, 8, 3, 1],
                           [2, 5, 5, 10, 10, 5, 5, 2],
                           [2, 5, 5, 9, 9, 5, 5, 2],
                           [1, 2, 5, 6, 6, 5, 2, 1],
                           [1, 2, 2, 3, 3, 2, 2, 1],
                           [0, 1, 2, 5, 5, 2, 1, 0]])

    PAWN_POS = np.array([[0,0,0,0,0,0,0,0],
                         [7,7,8,9,9,8,7,7],
                         [2.5,3.5,5,6.5,6.5,5,3.5,2.5],
                         [2,3,4,5,5,4,3,2],
                         [2,2.5,3.25,4,4,3.25,2.5,2],
                         [1,2,2,2.5,2.5,2,2,1],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0]])

    QUEEN_POS = np.array([[20, 0, 0, 35, 35, 0, 0, 20],
                          [0, 25, 0, 0, 0, 0, 25, 0],
                          [0, 0, 40, 0, 0, 40, 0, 0],
                          [27.5, 0, 0, 35, 35, 0, 0, 27.5],
                          [27.5, 0, 0, 35, 35, 0, 0, 27.5],
                          [0, 0, 30, 0, 0, 30, 0, 0],
                          [0, 25, 0, 20, 20, 0, 25, 0],
                          [20, 0, 0, 25, 25, 0, 0, 20]])

    BISHOP_POS = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 8, 10, 10, 8, 0, 0],
                           [0, 0, 0, 14, 14, 0, 0, 0],
                           [0, 0, 0, 14, 14, 0, 0, 0],
                           [0, 0, 12, 8, 8, 12, 0, 0],
                           [0, 10, 0, 0, 0, 0, 10, 0],
                           [0, 0, 0, 7, 7, 0, 0, 0]])

    ROOK_POS = np.array([[15, 0, 0, 25, 25, 0, 0, 15],
                         [10, 10, 15, 20, 20, 15, 10, 10],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 10, 10, 0, 0, 0],
                         [0, 0, 0, 10, 10, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [10, 0, 0, 15, 15, 0, 0, 10],
                         [0, 0, 0, 15, 15, 0, 0, 0]])

    def __init__(self, chess_game):
        self.chess_game = chess_game

    def move_turn(self):
        moves = self.chess_game.generate_valid_moveset()
        random.shuffle(moves)
        self.find_move(moves, 3, 3, -CHECKMATE, CHECKMATE, 1 if self.chess_game.turn == "w" else -1)
        global next_move
        if next_move is None:
            return
        print(count)
        self.chess_game.move(next_move)

    def find_move(self, valid_moves, depth, DEPTH,  alpha, beta, tm):
        if depth == 0:
            return tm * self.evaluate()
        # move ordering - implement later //TODO
        max_score = -CHECKMATE
        for move in valid_moves:
            self.chess_game.move(move, True)
            next_moves = self.chess_game.generate_valid_moveset()
            score = -self.find_move(next_moves, depth - 1, DEPTH, -beta, -alpha, -tm)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    global next_move
                    next_move = move
            self.chess_game.unmove()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    def evaluate(self):
        return self.evaluate_material()

    def evaluate_material(self):
        global count
        count = count + 1
        arr = self.chess_game.white_material
        score = 0.0
        wking = arr[1].pop()
        arr[1].add(wking)
        wking = "wK" + wking
        bking = self.chess_game.black_material[1].pop()
        self.chess_game.black_material[1].add(bking)
        bking = "bK" + bking
        if self.chess_game.checkmate(wking):
            return -CHECKMATE
        if self.chess_game.checkmate(bking):
            return CHECKMATE
        for i in arr[0]:
            score += ChessAi.MATERIAL["P"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score += ChessAi.PAWN_POS[ind[0]][ind[1]]
        for i in arr[2]:
            score += ChessAi.MATERIAL["N"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score += ChessAi.KNIGHT_POS[ind[0]][ind[1]]
        for i in arr[3]:
            score += ChessAi.MATERIAL["Q"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score += ChessAi.QUEEN_POS[ind[0]][ind[1]]
        for i in arr[4]:
            score += ChessAi.MATERIAL["R"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score += ChessAi.ROOK_POS[ind[0]][ind[1]]
        for i in arr[5]:
            score += ChessAi.MATERIAL["B"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score += ChessAi.BISHOP_POS[ind[0]][ind[1]]
        arr = self.chess_game.black_material
        for i in arr[0]:
            score -= ChessAi.MATERIAL["P"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score -= ChessAi.PAWN_POS[ind[0]][ind[1]]
        for i in arr[2]:
            score -= ChessAi.MATERIAL["N"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score -= ChessAi.KNIGHT_POS[ind[0]][ind[1]]
        for i in arr[3]:
            score -= ChessAi.MATERIAL["Q"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score -= ChessAi.QUEEN_POS[ind[0]][ind[1]]
        for i in arr[4]:
            score -= ChessAi.MATERIAL["R"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score -= ChessAi.ROOK_POS[ind[0]][ind[1]]
        for i in arr[5]:
            score -= ChessAi.MATERIAL["B"]
            ind = convert(i) if self.chess_game.turn == "w" else flip(convert(i))
            score -= ChessAi.BISHOP_POS[ind[0]][ind[1]]
        return score

def convert_s(symbol):
    return ord(symbol) - 97


def convert_n(num):
    return 8 - int(num)


def convert(move):
    x1 = int(convert_n(move[1]))
    y1 = int(convert_s(move[0]))
    return [x1, y1]


def flip(ind):
    return [7-ind[0], 7-ind[1]]
