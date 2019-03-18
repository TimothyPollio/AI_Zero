import numpy as np
from Game.symmetry import Rotation, Reflection

EMPTY_BOARD      = np.zeros((2,9))
FLAT_BOARD_SHAPE = [2,9]
TRUE_BOARD_SHAPE = [2,3,3]
POLICY_SIZE      = 9

winners = [[0,1,2],[3,4,5],[6,7,8],
           [0,3,6],[1,4,7],[2,5,8],
           [0,4,8],[2,4,6]]

def direct_evaluate(board):
    for trip in winners:
        if all(board[0][i] for i in trip):
            return 1
        if all(board[1][i] for i in trip):
            return -1
    if board.sum() == 9:
        return 0
    return "NOT DONE"

def legal_moves(board):
    taken = board.sum(axis=0)
    return [i for i in range(9) if not taken[i]]

def get_turn(board):
    return int(board.sum()) % 2

def board_after(board, move, player=None):
    if not player:
        player = get_turn(board)
    out = board.copy()
    out[player][move] = 1
    return out

# Symmetries
tau = Rotation(3)
sigma = Reflection(3,3)
SYMMETRIES = [sigma ** n for n in range(1,4)] + [tau * sigma ** n for n in range(0,4)]

# Externally generated test set (for diagnostic only)
TEST_POSITIONS = np.load("./Game/tic_reference/positions").reshape(-1,2,9)
TEST_VALUES = np.load("./Game/tic_reference/labels").reshape(-1,1)
