import numpy as np
from functools import reduce

from constants import (RECORD_HISTORY, CULL_THRESHOLD, GAMES_PER_CYCLE,
                       VERBOSE_MCTS, STEPS_PER_MOVE, NOISE_TYPE, NOISE_VALUE)
from Core.record import Record, combine_records
from Core.tree import Tree
from Game import board_after, direct_evaluate, get_children, is_done, EMPTY_BOARD, SYMMETRIES

class Game():

    def __init__(self, start_position, to_play = 0):
        self.position_stack = []
        self.policy_stack   = []
        self.history_stack  = [[]]
        self.position       = start_position
        self.to_play        = to_play
        self.latest_move    = None
        self.finished       = False
        self.tree           = None

    def update(self, move, policy_vector):
        self.position_stack.append(self.position)
        self.policy_stack.append(policy_vector)
        if RECORD_HISTORY:
            self.history_stack.append(self.history_stack[-1] + [str(move)])
        self.position = board_after(self.position, move, self.to_play)
        self.to_play = (self.to_play + 1) % 2
        self.latest_move = move

        if is_done(self.position):
            self.finished = True
            self.winner = direct_evaluate(self.position)
            self.record = Record(positions = np.array(self.position_stack),
                                 values    = np.repeat([[self.winner]],
                                                       len(self.policy_stack),
                                                       axis=0),
                                 policies = np.array(self.policy_stack),
                                 history  = self.history_stack)
            self.record.cull(CULL_THRESHOLD)

class MultipleSelfPlay():
    '''
    Combines the MCTS and Neural Network code to execute multiple self-play games in parallel.
    While playing the games in sequence would have been easier to code, this approach improves
    performance by allowing us to feed positions to the neural network in batches.
    '''
    def __init__(self, players, number_of_games = GAMES_PER_CYCLE):

        if isinstance(players, list):
            self.players = players
            self.reuse_trees = False
        else:
            self.players = [players, players]
            self.reuse_trees = True

        self.tournament = False
        self.moves_played = 0
        self.games = [Game(EMPTY_BOARD) for _ in range(number_of_games)]
        self.active_games = self.games

    def play(self):
        while self.active_games:
            self.play_move()
        return self

    def play_move(self):
        player = self.players[self.moves_played % 2]

        if player.use_mcts:
            player.set_temperature(self.tournament, self.moves_played)
            self.setup_trees()
            self.mcts(player)
        for game in self.active_games:
            game.update(*player.get_move(game))

        self.moves_played += 1
        self.active_games = [game for game in self.games if not game.finished]
        if VERBOSE_MCTS and self.moves_played % 10 == 0:
            print("SELF PLAY AT DEPTH", self.moves_played)

    def setup_trees(self):
        if self.reuse_trees and self.active_games[0].latest_move:
            for game in self.active_games:
                game.tree = game.tree.get_child(game.latest_move)
        else:
            parity = -1 if (self.moves_played % 2) else 1
            for game in self.active_games:
                game.tree = Tree(game.position, parity = parity)

    def mcts(self, player):
        trees = [game.tree for game in self.active_games]
        for _ in range(STEPS_PER_MOVE):
            eval_buffer = [tree.get_next() for tree in trees]
            values, policies = player.predict(eval_buffer)

            for tree, value, policy in zip(trees, values, policies):
                tree.expand_and_update(value, policy)

    def record(self, use_symmetry = True):
        rec = reduce(combine_records, (game.record for game in self.games))
        if use_symmetry:
            augmented_rec = [rec] + [s * rec for s in SYMMETRIES]
            return reduce(combine_records, augmented_rec)
        return rec

    def score(self):
        player1_wins = len([game for game in self.games if game.winner == 1])
        player1_losses = len([game for game in self.games if game.winner == -1])
        ties = len(self.games) - player1_wins - player1_losses
        score = (player1_wins - player1_losses) / len(self.games)
        print("Win-Tie-Loss:", player1_wins, "-", ties, "-", player1_losses)
        return score

class Tournament(MultipleSelfPlay):

    def __init__(self, players):
        self.tournament = True
        self.players = players
        self.reuse_trees = False
        self.moves_played = 2
        self.games = [Game(position) for child in get_children(EMPTY_BOARD)\
                                     for position in get_children(child)]
        self.active_games = self.games

def compare_players(players):
    score1 = Tournament(players).play().score()
    score2 = Tournament(players[::-1]).play().score()
    score = (score1 - score2) / 2
    print("Score:", score)
    return score
