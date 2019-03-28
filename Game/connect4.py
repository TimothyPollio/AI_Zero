'''
Square/move names:

0   1   2   3   4   5   6
7   8   9   10  11  12  13
14  15  16  17  18  19  20
21  22  23  24  25  26  27
28  29  30  31  32  33  34
35  36  37  38  39  40  41
'''
import numpy as np
from Game.symmetry import Reflection

EMPTY_BOARD      = np.zeros((2, 42))
FLAT_BOARD_SHAPE = [2, 42]
TRUE_BOARD_SHAPE = [2, 6, 7]
POLICY_SIZE      = 42

horizontal = [0,  1,  2,  3]
vertical   = [0,  7,  14, 21]
diagonal1  = [0,  8,  16, 24]
diagonal2  = [21, 15, 9,  3]

quads = [horizontal, vertical, diagonal1, diagonal2]

winners = [[base+i+7*j for base in quads[index]] for index in range(4)\
                                                 for i in range([4, 7, 4, 4][index])\
                                                 for j in range([6, 3, 3, 3][index])]

# Vectorization to speed up the win check is important since it's repeated MANY times
winners_matrix = np.array([[1 if i in quad else 0 for i in range(42)] for quad in winners])

def direct_evaluate(board):
    if np.any(np.matmul(winners_matrix, board[0]) == 4):
        return 1
    if np.any(np.matmul(winners_matrix, board[1]) == 4):
        return -1
    if board.sum() == 42:
        return 0
    return "NOT DONE"

def legal_moves(board):
    sum_ = board.sum(axis=0).reshape(6,7).sum(axis=0)
    cols = [i for i in range(7) if sum_[i]<6]
    return [int(35 + c - 7 * sum_[c]) for c in cols]

def get_turn(board):
    return int(board.sum()) % 2

def board_after(board, move, player = None):
    move = move % 7
    if not player:
        player = get_turn(board)
    out = board.copy()
    sum_ = out.sum(axis=0)
    for y in range(35,-1,-7):
        if not sum_[y + move]:
            out[player][y + move] = 1
            return out

def board_from_string(game_history):
    if game_history in ["START", "", None]:
        return EMPTY_BOARD
    move_list = game_history.split("-")
    board = EMPTY_BOARD.copy()
    for n, move in enumerate(move_list):
        board[n % 2][int(move)] = 1
    return board

# Symmetries
SYMMETRIES = [Reflection(6, 7)]
