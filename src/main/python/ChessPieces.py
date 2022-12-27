import numpy as np


def check_bishop(move,game):
    coords = convert(move)
    if not abs(coords[0]-coords[2]) == abs(coords[1]-coords[3]):
        return False
    xInc = 1 if coords[2]-coords[0] > 0 else -1
    yInc = 1 if coords[3] - coords[1] > 0 else -1
    return bishop_help(coords, game, xInc, yInc, move[0])


def bishop_help(coords, game, x_inc, y_inc, is_white):
    for i in range(abs(coords[0]-coords[2])-1):
        coords[0] += x_inc
        coords[1] += y_inc
        if not game[coords[0]][coords[1]] == "--":
            return False
    return game[coords[2]][coords[3]] == "--" or not game[coords[2]][coords[3]][0] == is_white


def check_pawn(move, game, moves, pawns):
    coords = convert(move)
    xDif = abs(coords[0] - coords[2])
    yDif = abs(coords[1] - coords[3])
    is_white = -1 if move[0] == "w" else 1
    if yDif == 0 and xDif == 1:
        return game[coords[2]][coords[3]] == "--" and is_white == coords[2] - coords[0]
    elif yDif == 0 and xDif == 2 and is_white*2 == coords[2] - coords[0]:
        row = 0 if move[0] == "w" else 1
        inc = -1 if move[0] == "w" else 1
        return (not pawns[row][coords[1]]) and game[coords[0]+inc][coords[1]] == "--" and game[coords[0]+inc*2][coords[1]] == "--" and (move[3] == "7" or move[3] == "2")
    elif yDif == 1 and xDif == 1 and is_white == coords[2] - coords[0]:
        if game[coords[2]][coords[3]] == "--":
            prevMove = moves[len(moves)-1]
            coords2 = convert(prevMove)
            return abs(coords2[2] - coords2[0]) == 2 and coords2[3] == coords[3] and coords2[2]+is_white == coords[2]
        else:
            return not game[coords[2]][coords[3]][0] == move[0]
         # EnPassant, Normal, Check if Moving in Right Direction
    return False


def check_rook(move, game):
    coords = convert(move)
    if not abs(coords[0] - coords[2]) == 0 and not abs(coords[1] - coords[3]) == 0:
        return False
    xInc = 0 if abs(coords[0] - coords[2]) == 0 else 1 if coords[2] - coords[0] > 0 else -1
    yInc = 0 if abs(coords[3] - coords[1]) == 0 else 1 if coords[3] - coords[1] > 0 else -1
    return rook_help(coords, game, xInc, yInc, move[0])


def rook_help(coords, game, x_inc, y_inc, is_white):
    for i in range(max(abs(coords[0]-coords[2]),abs(coords[3]-coords[1]))-1):
        coords[0] += x_inc
        coords[1] += y_inc
        if not game[coords[0]][coords[1]] == "--":
            return False
    return game[coords[2]][coords[3]] == "--" or not game[coords[2]][coords[3]][0] == is_white


def check_queen(move, game):
    return check_bishop(move, game) or check_rook(move, game)


def check_king(move, game, rooks):
    coords = convert(move)
    xDif = abs(coords[0] - coords[2])
    yDif = abs(coords[1] - coords[3])
    is_white = "b" if move[0] == "b" else "w"
    if yDif == 2 and xDif == 0:
        return check_castle(coords, game, is_white, rooks)
    elif yDif == 1 and xDif == 1:
        return game[coords[2]][coords[3]] == "--" or not is_white == game[coords[2]][coords[3]][0]
    return False


def check_castle(coords, game, is_white, rooks):
    row = 0 if is_white == "b" else 2
    squaresToCheck = 3 if coords[3] - coords[1] < 0 else 2
    inc = -1 if squaresToCheck == 3 else 1
    for i in range(squaresToCheck):
        coords[1] += inc
        if not game[coords[0]][coords[1]] == "--":
            return False
    add = 0 if squaresToCheck == 3 else 1
    row += add
    return not rooks[row]


def check_knight(move, game):
    coords = convert(move)
    xDif = abs(coords[0]-coords[2])
    yDif = abs(coords[1]-coords[3])
    if not (xDif == 2 and yDif == 1) or (xDif == 1 and yDif == 2):
        return False
    is_white = move[0]
    return game[coords[2]][coords[3]] == "--" or not game[coords[2]][coords[3]][0] == is_white


def convert_s(symbol):
    return ord(symbol) - 97


def convert_n(num):
    return 8-int(num)


def convert(move):
    x1 = int(convert_n(move[3]))
    y1 = int(convert_s(move[2]))
    x2 = int(convert_n(move[5]))
    y2 = int(convert_s(move[4]))
    return [x1, y1, x2, y2]


def valid_rook(coords, board):
    xy = [convert_n(coords[3]), convert_s(coords[2])]
    is_white = coords[0]
    return check_direction(xy, is_white, board, 1, 0) + check_direction(xy, is_white, board, -1, 0) + check_direction(
        xy, is_white, board, 0, -1) + check_direction(xy, is_white, board, 0, 1)


def valid_bishop(coords, board):
    xy = [convert_n(coords[3]), convert_s(coords[2])]
    is_white = coords[0]
    return check_direction(xy, is_white, board, 1, 1) + check_direction(xy, is_white, board, -1, -1) + check_direction(
        xy, is_white, board, 1, -1) + check_direction(xy, is_white, board, -1, 1)


def valid_queen(coords, board):
    return valid_bishop(coords, board) + valid_rook(coords, board)


def valid_knight(coords, board):
    moves = [[1,2],[2,1],[-1,2],[2,-1],[-1,-2],[-2,-1],[1,-2],[-2,1]]
    ans = []
    xy = [convert_n(coords[3]), convert_s(coords[2])]
    is_white = coords[0]
    for move in moves:
        x = xy[0] + move[0]
        y = xy[1] + move[1]
        if in_bounds(x, y) and board[x][y][0] != is_white:
            ans.append((x, y))
    return ans


def in_bounds(x, y):
    return 8 > x >= 0 and 8 > y >= 0


def valid_king(coords, board, moved):
    ans = []
    x = convert_n(coords[3])
    y = convert_s(coords[2])
    is_white = coords[0]
    for i in range(-1, 2):
        x1 = x + i
        for j in range(-1, 2):
            y1 = y + j
            if in_bounds(x1,y1) and board[x1][y1][0] != is_white:
                ans.append((x1, y1))
    orig = 7 if is_white == "w" else 0
    ind = 4 if is_white == "w" else 5
    ind1 = 2 if is_white == "w" else 0
    c = coords + "g" + str(8-orig)
    if not moved[ind] and board[orig][0][1] == "R" and not moved[ind1] and check_castle(convert(c), board, is_white, moved):
        ans.append((orig, 2))
    c = coords + "c" + str(8 - orig)
    if not moved[ind] and board[orig][7][1] == "R" and not moved[ind1+1] and check_castle(convert(c), board, is_white, moved):
        ans.append((orig, 6))
    return ans


def check_direction(xy, is_white, board, x_inc, y_inc):
    ans = []
    x = xy[0]
    y = xy[1]
    for i in range(8):
        x += x_inc
        y += y_inc
        if x < 0 or x > 7 or y < 0 or y > 7:
            return ans
        temp = board[x][y]
        if (not temp == "--") and (temp[0] == is_white):
            return ans
        if (not temp == "--") and (temp[0] != is_white):
            ans.append((x, y))
            return ans
        ans.append((x, y))


def valid_pawn(coords, board, moves, movedPawns):
    ans = []
    is_white = coords[0]
    first = 6 if is_white == "w" else 1
    inc = -1 if is_white == "w" else 1
    ind = 0 if is_white == "w" else 1
    x = convert_n(coords[3])
    y = convert_s(coords[2])
    if board[x+inc][y] == "--":
        ans.append((x+inc, y))
    if first == x and not movedPawns[ind][y] and board[x+inc*2][y] == "--" and board[x+inc][y] == "--":
        ans.append((x+inc*2, y))
    if in_bounds(x + inc, y - 1) and not board[x + inc][y-1] == "--" and not board[x + inc][y - 1][0] == is_white:
        ans.append((x + inc, y - 1))
    if in_bounds(x + inc, y + 1) and not board[x + inc][y+1] == "--" and not board[x + inc][y + 1][0] == is_white:
        ans.append((x + inc, y + 1))
    if len(moves) == 0:
        return ans
    prev = moves[len(moves)-1]
    x1 = convert_n(prev[5])
    y1 = convert_s(prev[4])
    if board[x1][y1][1] == "P" and not board[x1][y1][0] == is_white and x1 == x and abs(y1-y) == 1 and \
            board[x1+inc][y1] == "--":
        ans.append((x+inc, y1))
    return ans


def axis(board, x, y,  x_inc, y_inc, piece, color):
    queen = color + "Q"
    for i in range(7):
        x += x_inc
        y += y_inc
        if not in_bounds(x, y):
            return False
        if board[x][y] == piece or board[x][y] == queen:
            return True
        if not board[x][y] == "--":
            return False
    return False


board = [["bR", "--", "--", "--", "bK", "--", "--", "bR"],
         ["wP", "bP", "wP", "--", "--", "wB", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "wB", "--", "--", "--", "--"],
         ["--", "--", "wB", "wN", "wB", "--", "wP", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wP", "bP", "--", "--", "--", "wP", "--", "--"],
         ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]

arr = [[False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False,]]
print(valid_pawn("bPb7", board, ["wPc6c7"], arr))
