### General
GAME         = 'Connect4'
VERSION_NAME = 'Connect4-V1'
WARM_START   = False

### Network
NUM_FILTERS    = 92
FILTER_SIZE    = [4,4]
NUM_RES_BLOCKS = 2
HIDDEN_SIZE    = 128  # For value head

### MCTS / Self-play
GAMES_PER_CYCLE         = 64
STEPS_PER_MOVE          = 128
EXPLORATION_TEMPERATURE = 1          # Initial temperature for MCTS
FINAL_TEMPERATURE       = 0.1
EXPLORATION_THRESHOLD   = 10         # Temperature set to above after this many moves
RANDOM_THRESHOLD        = 4          # First N moves are played randomly
NOISE_TYPE              = "constant"
NOISE_VALUE             = 0.3
EXPLORATION_CONSTANT    = 1          # Weight for P in MCTS
EPSILON                 = 10 ** -6   # Small constant to avoid division by 0
VERBOSE_MCTS            = True

### Record
MAX_RECORD_SIZE = 100000
MIN_RECORD_SIZE = 30000
CULL_THRESHOLD  = 4  # Positions with very low depth are omitted from record
RECORD_HISTORY  = False
RECORD_MCTS     = True

### Training
ALPHA                   = 0.0001
LEARNING_RATE           = 0.005
BATCH_SIZE              = 256
BATCHES_PER_CYCLE       = 40
MAX_EPOCHS_PER_CYCLE    = 1
VERBOSE_TRAINING        = False
METRIC_REPORT_FREQUENCY = 1
SAVE_FREQUENCY          = 25
REFERENCE_AVAILABLE     = False
