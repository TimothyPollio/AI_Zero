import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from constants import *
from Core.player import NetworkPlayer
from Core.record import combine_records
from Core.self_play import MultipleSelfPlay

if REFERENCE_AVAILABLE:
    from Game import TEST_POSITIONS, TEST_VALUES, POLICY_SIZE

player = NetworkPlayer()
game_record = None

def self_play():
    global game_record
    game_record = combine_records(game_record,
                                  MultipleSelfPlay(player).play().record())
    if len(game_record) > MAX_RECORD_SIZE:
        game_record.cull(len(game_record) - MAX_RECORD_SIZE)
    print("Game record now has size", len(game_record))

def train():
    global game_record
    for n in range(min(BATCHES_PER_CYCLE,
                       int(len(game_record) * MAX_EPOCHS_PER_CYCLE / BATCH_SIZE))):
        player.train(*game_record.batch())
        if VERBOSE_TRAINING and n > 1 and n % 100 == 0:
            print("TRAINING ON BATCH", n)

def print_metrics(step):
    global game_record
    metrics = player.metrics(*game_record.batch())
    print("Step {} Loss: {:.3f} Policy Loss: {:.3f} Value Loss: {:.3f} Value Accuracy: {:.1f}%"\
                 .format(*((step,) + tuple(metrics))))
    if REFERENCE_AVAILABLE:
        dummy_policy = np.zeros((TEST_VALUES.size, POLICY_SIZE))
        test_metrics = player.metrics(TEST_POSITIONS, TEST_VALUES, dummy_policy)
        print("True Value Loss: {:.3f} True Value Accuracy: {:.1f}%".format(test_metrics[-2], test_metrics[-1]))

if __name__ == '__main__':

    print("Generating record...")
    self_play()
    while len(game_record) < MIN_RECORD_SIZE:
        self_play()

    print("Training...")
    step = 0
    while True:
        step += 1
        train()
        if step % METRIC_REPORT_FREQUENCY == 0:
            print_metrics(step)
        self_play()
