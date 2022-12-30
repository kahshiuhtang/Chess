import random

next_move = None
class ChessAi:
    MATERIAL = {"P": 10.0, "R": 50.0, "Q": 100.0, "K": 10000, "N": 27.5, "B": 30.0}
    DEPTH = 2

    def __init__(self, chess_game):
        self.chess_game = chess_game

    def move_turn(self):
        moves = self.chess_game.generate_valid_moveset()
        random.shuffle(moves)
        self.find_move(moves, 2, 2, -100000, 100000, 1 if self.chess_game.turn == "w" else -1)
        global next_move
        print(next_move)
        DEPTH = 2 #Change to be more generic
        if next_move is None:
            return
        self.chess_game.move(next_move)

    def find_move(self, valid_moves, depth, DEPTH,  alpha, beta, tm):
        global next_move
        if depth == 0:
            return tm * self.evaluate()
        # move ordering - implement later //TODO
        max_score = -100000
        for move in valid_moves:
            self.chess_game.move(move, True)
            next_moves = self.chess_game.generate_valid_moveset()
            score = -self.find_move(next_moves, depth - 1, DEPTH, -beta, -alpha, -tm)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
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
        arr = self.chess_game.black_material if self.chess_game.turn == "b" else self.chess_game.white_material
        score = 0.0
        for i in arr[0]:
            score += ChessAi.MATERIAL["P"]
        for i in arr[2]:
            score += ChessAi.MATERIAL["N"]
        for i in arr[3]:
            score += ChessAi.MATERIAL["Q"]
        for i in arr[4]:
            score += ChessAi.MATERIAL["R"]
        for i in arr[5]:
            score += ChessAi.MATERIAL["B"]
        return score
