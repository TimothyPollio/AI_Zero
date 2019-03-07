import tensorflow as tf

from constants import (EXPLORATION_TEMPERATURE, FINAL_TEMPERATURE,
                       EXPLORATION_THRESHOLD, RANDOM_THRESHOLD)
from Core.network import (sess, train, value, policy, loss, policy_loss, value_loss,
                         value_accuracy, load_model, board_positions,
                         policy_labels, value_labels, training)

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
