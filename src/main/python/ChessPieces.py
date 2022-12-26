
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
        return check_castle(coords, game, is_white, rooks, move)
    elif yDif == 1 and xDif == 1:
        return game[coords[2]][coords[3]] == "--" or not is_white == game[coords[2]][coords[3]][0]
    return False


def check_castle(coords, game, is_white, rooks, move):
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
    return (ord(symbol) - 97)


def convert_n(num):
    return 8-int(num)


def convert(move):
    x1 = int(convert_n(move[3]))
    y1 = int(convert_s(move[2]))
    x2 = int(convert_n(move[5]))
    y2 = int(convert_s(move[4]))
    return [x1, y1, x2, y2]


