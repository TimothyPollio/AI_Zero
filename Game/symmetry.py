import numpy as np
from functools import reduce
from Core.record import Record

class Symmetry():

    def __init__(self, transform_dict):
        self.dict = transform_dict
        self.N = len(self.dict)
        self.matrix = np.zeros((self.N, self.N))
        for i in range(self.N):
            self.matrix[i][transform_dict[i]] = 1

    def __mul__(self, other):
        if isinstance(other, np.ndarray):
            return other.dot(self.matrix)
        if isinstance(other, list):
            return [[str(self.dict[int(m)]) for m in hist] for hist in other]
        if isinstance(other, Record):
            return Record(self * other.pos, other.val, self * other.pol, self * other.hst)
        if isinstance(other, Symmetry):
            return Symmetry({i: self.dict[other.dict[i]] for i in range(self.N)})
        if other == 1:
            return self

    def __pow__(self, n):
        if n == 0:
            return 1
        else:
            return reduce(lambda x, y: x * y, [self for _ in range(n)])

def Rotation(board_width):
    '''
    90° rotation (square boards only)
    '''
    transform_dict = {}
    for m in range(board_width ** 2):
        row, column = m // board_width, m % board_width
        row, column = column, board_width - row - 1
        transform_dict[m] = row * board_width + column
    return Symmetry(transform_dict)

def Reflection(board_width, board_height):
    '''
    Reflection across vertical axis of symmetry
    '''
    transform_dict = {}
    for col in range(board_width):
        for row in range(board_height):
            transform_dict[row * board_width + col] = (row + 1) * board_width - (col + 1)
    return Symmetry(transform_dict)
