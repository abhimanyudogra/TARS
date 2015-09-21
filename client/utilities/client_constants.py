# Window properties
WINDOW_X = 1280
WINDOW_Y = 768

# Radar constants
OFFSET_X, OFFSET_Y = WINDOW_X / 2, WINDOW_Y / 2
SCALE = 8
OBJECT_SIZE = 4
OFFSET_OBJECT = SCALE / 2 - OBJECT_SIZE / 2
BOT = "bot"
WALL = "wall"
SHORTEST_PATH = "shortest_path"
HIGHLIGHT = "highlight"

# GPIO motor movement constants
STOP = (0, 0)
LEFT = (1, 2)
RIGHT = (2, 1)
FORWARD = (1, 1)

# Bot direction constants
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

MOTOR_TURN_TIME_90 = 0.4
MOTOR_MOVE_10_CM_TIME = 2

# Raspberry network constants
TARS_IP = "127.0.0.1"
PORT = 5000  # Arbitrary non-privileged port

# Communication message commands
STARTUP = "startup"
SHUTDOWN = "shutdown"
MOTOR_CHANGE = "motor_change"
DETECT_OBSTACLE = "detect_obstacle"
