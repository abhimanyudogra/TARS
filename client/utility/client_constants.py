__author__ = "Niharika Dutta and Abhimanyu Dogra"

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

# Communication message commands
STARTUP = "@startup"
SHUTDOWN = "@shutdown"
MOTOR_CHANGE = "@motor_change"
STANDBY = "@standby"
DETECT_OBSTACLE = "@detect_obstacle"
DELIMITER = "@"

DESTINATION_FOUND = "found"
DESTINATION_BLOCKED = "blocked""unreachable"
DESTINATION_UNREACHABLE = "unreachable"
MANUAL_EXIT = "exit"
