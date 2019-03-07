### General
GAME         = 'Tic-Tac-Toe'
VERSION_NAME = 'Tic-V1'
WARM_START   = False

### Network
NUM_FILTERS    = 32
FILTER_SIZE    = [3,3]
NUM_RES_BLOCKS = 1
HIDDEN_SIZE    = 32  # For value head

### MCTS / Self-play
GAMES_PER_CYCLE         = 32
STEPS_PER_MOVE          = 40
EXPLORATION_TEMPERATURE = 1          # Initial temperature for MCTS
FINAL_TEMPERATURE       = 0.1
EXPLORATION_THRESHOLD   = 4          # Temperature set to above after this many moves
RANDOM_THRESHOLD        = 2          # First N moves are played randomly
NOISE_TYPE              = "constant"
NOISE_VALUE             = 0.2
EXPLORATION_CONSTANT    = 1          # Weight for P in MCTS
EPSILON                 = 10 ** -6   # Small constant to avoid division by 0
VERBOSE_MCTS            = True

### Record
MAX_RECORD_SIZE = 20 * 256
MIN_RECORD_SIZE = 0 * 256
CULL_THRESHOLD  = 2  # Positions with very low depth are omitted from record
RECORD_HISTORY  = True

### Training
ALPHA                   = 0.0001
LEARNING_RATE           = 0.005
BATCH_SIZE              = 128
BATCHES_PER_CYCLE       = 100
MAX_EPOCHS_PER_CYCLE    = 1
VERBOSE_TRAINING        = True
METRIC_REPORT_FREQUENCY = 1
TOURNAMENT_FREQUENCY    = 15
REFERENCE_AVAILABLE     = False
