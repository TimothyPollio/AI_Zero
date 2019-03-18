import numpy as np

from constants import EXPLORATION_CONSTANT, EPSILON
from Game import is_done, direct_evaluate, legal_moves, board_after, POLICY_SIZE

class Tree():

    def __init__(self, position, Q = 0, P = 0, parity = 1, parent = None, move = None):
        self.position = position
        self.parent   = parent
        self.move     = move   # Most recent move (if not root)
        self.parity   = parity # 1 if Player 1 has the move, else -1
        self.Q        = Q      # Note: Correct initial value is 0, not parent.Q
        self.P        = P
        self.U        = EXPLORATION_CONSTANT * P
        self.N        = 0
        self.sN       = 1 # sqrt(self.N + 1); used as a multiplier for child.U

    def get_next(self):
        '''
        Iteratively chooses the node with the greatest action value until an unexplored node is reached,
        then returns the corresponding position to be evlauted by the neural network.
        The path from the root is stored in self.stack so that Q values can be updated later.
        '''
        self.stack = [self]
        node = self
        while node.N and not is_done(node.position):
            node = max(node.children, key = lambda child: node.parity * child.Q\
                                                        + child.U * node.sN)
            self.stack.append(node)
        return node.position

    def expand_and_update(self, value, policy):
        '''
        Expands the tree by adding positions below the current node, then updates values for all nodes
        in self.stack using the evaluation done by the neural network.
        '''
        node = self.stack[-1]

        ### Expand
        if is_done(node.position):
            node.Q = direct_evaluate(node.position)
            # Override priors for previous two half-moves when a winning position is found
            if node.Q != 0:
                node.P = 100
                if node.parent:
                    node.parent.P = -100
        else:
            node.Q = value[0]
            policy = policy / (sum(policy[i] for i in legal_moves(node.position)) + EPSILON)
            to_play = 0 if node.parity == 1 else 1
            node.children = [Tree(position = board_after(node.position, m, to_play),
                                  P = policy[m],
                                  parity = node.parity * -1,
                                  parent = node,
                                  move = m) for m in legal_moves(node.position)]
        ### Update
        new_Q = node.Q
        while self.stack:
            node = self.stack.pop()
            if node.N:
                node.Q = (node.Q * node.N + new_Q) / (node.N + 1.)
            node.N += 1
            node.sN = np.sqrt(node.N + 1)
            node.U = EXPLORATION_CONSTANT * node.P / (node.N + 1.)

    def choose_move(self, temperature = 1):
        '''
        Returns a move choice and policy vector based on the current state of the tree.
        '''
        policy_vector = np.zeros(POLICY_SIZE)
        for child in self.children:
            policy_vector[child.move] = child.N

        if temperature not in [0, 1, "random"]:
            policy_vector = policy_vector ** (1 / temperature)
        policy_vector = policy_vector / policy_vector.sum()

        if temperature == 0:
            move = np.argmax(policy_vector)
        elif temperature == "random":
            move = np.random.choice(legal_moves(self.position))
        else:
            move = np.random.choice(POLICY_SIZE, p = policy_vector)

        return move, policy_vector

    def get_child(self, m):
        '''
        Returns subtree after given move.
        '''
        for child in self.children:
            if child.move == m:
                return child
