import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, render_template, send_from_directory

from constants import *
from Core.network import load_model
from Core.player import NetworkPlayer
from Core.self_play import MultipleSelfPlay

player = NetworkPlayer()
load_model()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('play.html')

@app.route('/src/<path:filename>')
def serve_file(filename):
    return send_from_directory('./src', filename)

@app.route('/get_move/<game_history>')
def choose_move(game_history):
    tree = player.analyze(game_history)
    move, _ = tree.choose_move(temperature = 0)
    return str(move)

@app.route('/tree/<game_history>')
def make_tree(game_history):
    tree = player.analyze(game_history)
    return render_template('tree.html', tree_data = tree.json(game_history))

if __name__ == "__main__":
    app.run()
