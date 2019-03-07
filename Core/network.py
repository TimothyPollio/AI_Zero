import os
import numpy as np
import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError, NotFoundError

from Game import FLAT_BOARD_SHAPE, TRUE_BOARD_SHAPE, POLICY_SIZE
from constants import (ALPHA, NUM_FILTERS, FILTER_SIZE, NUM_RES_BLOCKS,
                       HIDDEN_SIZE, VERSION_NAME, LEARNING_RATE)

sess = tf.Session()

board_positions = tf.placeholder(tf.float32, shape = [None] + FLAT_BOARD_SHAPE)
board_reshaped  = tf.reshape(board_positions, [-1] + TRUE_BOARD_SHAPE)

value_labels    = tf.placeholder(tf.float32, shape = [None, 1])
policy_labels   = tf.placeholder(tf.float32, shape = [None, POLICY_SIZE])

training        = tf.placeholder(tf.bool)

def conv_block(z, num_filters = NUM_FILTERS,
                  filter_size = FILTER_SIZE,
                  relu = True):
    w = tf.layers.conv2d(z, num_filters, filter_size, padding = "same")
    w = tf.layers.batch_normalization(w, training = training)
    if relu:
        w = tf.nn.relu(w)
    return w

### Convolutional Block
x = conv_block(board_reshaped)

### Residual Blocks
for _ in range(NUM_RES_BLOCKS):
    y = conv_block(x)
    y = conv_block(y, relu = False)
    x = tf.nn.relu(x + y)

### Policy Head
p = conv_block(x, 2, [1,1])
p = tf.contrib.layers.flatten(p)
policy_logits = tf.layers.dense(p, POLICY_SIZE, activation = None,
                                kernel_initializer = tf.zeros_initializer,
                                kernel_regularizer = tf.contrib.layers.l2_regularizer(scale = ALPHA))
policy = tf.nn.softmax(policy_logits)

### Value head
v = conv_block(x, 1, [1,1])
v = tf.contrib.layers.flatten(v)
v = tf.layers.dense(v, HIDDEN_SIZE, activation = tf.nn.relu,
                    kernel_initializer = tf.truncated_normal_initializer(1 / np.sqrt(NUM_FILTERS)),
                    kernel_regularizer = tf.contrib.layers.l2_regularizer(scale = ALPHA))
value = tf.layers.dense(v, 1, activation = tf.nn.tanh,
                        kernel_initializer = tf.zeros_initializer,
                        kernel_regularizer = tf.contrib.layers.l2_regularizer(scale = ALPHA))

### Accuracy & Loss
value_accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.round(value), value_labels), dtype=tf.float32))

reg_loss    = tf.losses.get_regularization_loss()
value_loss  = tf.reduce_mean(tf.square(value - value_labels))
policy_loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = policy_logits,
                                                                     labels = policy_labels))
loss = reg_loss + value_loss + policy_loss

### Training & Initialization
update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
with tf.control_dependencies(update_ops):
    train = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss)

print("Initializing...")
sess.run(tf.global_variables_initializer())

### Saving & Loading
saver = tf.train.Saver()

def file_path(file_name = "ckpt", loc = None):
    if not loc:
        loc = "./Models/" + VERSION_NAME
    if not os.path.exists(loc):
        os.makedirs(loc)
    return loc + "/" + file_name

def save_model(session = sess, msg = "model saved", loc = None):
    saver.save(session, file_path(loc = loc))
    if msg:
        print(msg)

def load_model(session = sess, msg = "model restored", loc = None):
    try:
        saver.restore(session, file_path(loc = loc))
        if msg:
            print(msg)
    except (InvalidArgumentError, NotFoundError):
        print("Warning: Failed to load old model")
        print("Running global variables initializer")
        session.run(tf.global_variables_initializer())
