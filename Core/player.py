import tensorflow as tf

from constants import (EXPLORATION_TEMPERATURE, FINAL_TEMPERATURE,
                       EXPLORATION_THRESHOLD, RANDOM_THRESHOLD)
from Core.network import (sess, train, value, policy, loss, policy_loss, value_loss,
                         value_accuracy, load_model, board_positions,
                         policy_labels, value_labels, training)

from Game import board_after, is_won, legal_moves

class NetworkPlayer():

    def __init__(self, session = sess):
        self.session  = session
        self.use_mcts = True

    def train(self, position_stack, value_stack, policy_stack):
        self.session.run(train, {board_positions: position_stack,
                                 value_labels: value_stack,
                                 policy_labels: policy_stack,
                                 training: True})

    def predict(self, position_stack, session = sess):
        return self.session.run([value, policy], {board_positions: position_stack,
                                                  training: False})

    def metrics(self, position_stack, value_stack, policy_stack, session = sess):
        return self.session.run([loss, policy_loss, value_loss, 100 * value_accuracy],
                                 {board_positions: position_stack,
                                 value_labels: value_stack,
                                 policy_labels: policy_stack,
                                 training: False})

    def set_temperature(self, tournament, move_number):
        if tournament:
            self.temperature = FINAL_TEMPERATURE
        else:
            if move_number >= EXPLORATION_THRESHOLD:
                self.temperature = FINAL_TEMPERATURE
            elif move_number >= RANDOM_THRESHOLD:
                self.temperature = EXPLORATION_TEMPERATURE
            else:
                self.temperature = "random"

    def get_move(self, game):
        return game.tree.choose_move(self.temperature)

class BackupNetPlayer(NetworkPlayer):

    def __init__(self, loc = None):
        self.session = tf.Session()
        load_model(self.session, msg = None, loc = loc)
        self.use_mcts = True

class ReferencePlayer():
    '''
    Weak player that relies on a shallow brute force search
    '''
    def __init__(self):
        self.use_mcts = False

    def get_move(self, game):
        board = game.position
        # Check for one move wins
        for m in legal_moves(board):
            if is_won(board_after(board, m)):
                return m, []
        # Otherwise take any move that doesn't lose immediately
        for m1 in legal_moves(board):
            board1 = board_after(board, m1)
            responses = legal_moves(board1)
            if not any(is_won(board_after(board1, m2)) for m2 in responses):
                return m1, []
        # Otherwise just play
        return legal_moves(board)[0], []
