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
CONFIRMATION = "confirmation"
DELIMITER = "@"
CLICK_PICTURE = "@click_picture"
IMAGES_SEQUENCE = ["left_pic", "middle_pic", "right_pic", "back_pic"]

SERVER_CONFIRMATION_TIMEOUT = 500

# Algorithm results
DESTINATION_FOUND = "found"
DESTINATION_BLOCKED = "blocked"
DESTINATION_UNREACHABLE = "unreachable"
MANUAL_EXIT = "exit"

# Connection results
TIMEOUT = "timeout"
CONNECTED = "connected"
UNCONNECTED = "unconnected"
CONNECTION_ERROR = "conn_err"
SOCKET_ERROR = "error"

# Menu buttons
CONNECT = "Connect"
SETTINGS = "Settings"
EXIT = "Exit"
RETRY = "Retry"
DISCONNECT = "Disconnect"
RECONNECT = "Reconnect"
DEPLOY = "Deploy"
CANCEL = "Cancel"

# States
ALPHA = "0"
BETA = "1"
GAMMA = "2"
DELTA = "3"
EPSILON = "4"
ZETA = "5"
ETA = "6"
THETA = "7"
IOTA = "8"

# Configurable
OBSTACLE_DISTANCE = "obstacle_distance"
DESTINATION_X = "dest_x"
DESTINATION_Y = "dest_y"
MOTOR_SPEED = "bot_speed"
BOT_TURN_TIME = "bot_turn_time"
MOTOR_TURN_SPEED = "bot_turn_speed"
BOT_INTER_NODE_TIME = "bot_inter_node_time"
WINDOW_WIDTH = "radar_x"
WINDOW_HEIGHT = "radar_y"
RADAR_SCALE = "radar_scale"
RASPBERRY_IP = "rasp_ip"
RASPBERRY_PORT = "rasp_port"
