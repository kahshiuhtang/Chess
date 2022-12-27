class ChessAi:
    MATERIAL = {"P": 10.0, "R": 50.0, "Q": 100.0, "K": 10000, "N": 30.0, "B": 30.0}
    def __init__(self, is_white):
        this.is_white = is_white

    def find_move(self, game, valid_moves, depth, a, b, tm):
        global next_move
        if depth == 0:
            return tm * evaluate(game)
        # move ordering - implement later //TODO
        max_score = -100000
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            game_state.undoMove()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    def evaluate(self, game):

    def evaluate_material(self, black, white):


