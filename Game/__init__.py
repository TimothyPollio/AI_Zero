from constants import GAME

if GAME == "Tic-Tac-Toe":
    from Game.tic import *

if GAME == "Connect4":
    from Game.connect4 import *

def get_children(board):
    return [board_after(board, move) for move in legal_moves(board)]

def is_done(board):
    return direct_evaluate(board) != "NOT DONE"

def is_won(board):
    return direct_evaluate(board) in [-1, 1]
