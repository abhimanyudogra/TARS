__author__ = "Niharika Dutta and Abhimanyu Dogra"

from copy import copy
import re

from PIL import Image
from images2gif import writeGif

from client.utility.client_constants import *


class DirectionHandler:
    """
    DirectionHandler class contains static methods for performing operations on N W S E directions
    like turning 90 degrees.
    """

    @staticmethod
    def turn_cw(direction):
        return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

    @staticmethod
    def turn_acw(direction):
        return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]


class Node:
    """
    Node class for tress and graphs.
    """

    def __init__(self, parent, heuristic, (x, y), path=[], parent_ancestors=set()):
        self.parent = parent
        self.heuristic = heuristic
        self.x = x
        self.y = y
        self.left = None
        self.front = None
        self.right = None
        self.ancestors = copy(parent_ancestors)
        if self.parent == -1:
            self.path = []
        else:
            self.path = copy(path)
            self.path.append((parent.x, parent.y))
            self.ancestors.add((parent.x, parent.y))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class GraphHandler:
    """
    GraphHandler class contains methods to perform common operations on graphs and trees
    """

    @staticmethod
    def find_common_ancestor(curr_node, next_node):
        path = copy(curr_node.path)
        path.reverse()
        for node in path:
            if node in next_node.ancestors:
                return node

    @staticmethod
    def create_path(curr_node, next_node, common_ancestor):
        common_ancestor_idx = curr_node.path.index(common_ancestor)
        subset = slice(common_ancestor_idx, len(curr_node.path))
        path1 = curr_node.path[subset]
        common_ancestor_idx = next_node.path.index(common_ancestor)
        subset = slice(common_ancestor_idx + 1, len(next_node.path))
        path2 = next_node.path[subset]
        path2.append((next_node.x, next_node.y))
        path1.reverse()
        path1.extend(path2)
        path1.insert(0, (curr_node.x, curr_node.y))
        return path1


datatypes = {
    int: {DESTINATION_X, DESTINATION_Y, MOTOR_SPEED, MOTOR_TURN_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT,
          RADAR_SCALE, RASPBERRY_PORT},
    float: {OBSTACLE_DISTANCE, BOT_TURN_TIME, BOT_INTER_NODE_TIME},
    str: {RASPBERRY_IP, }
}


class Config(object):
    """
    Config class stores all configurable variables.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        for (datatype, pool) in datatypes.items():
            if key in pool:
                try:
                    value = datatype(value)
                    self.validate(key, value)
                    self.__dict__[key] = value
                except ValueError:
                    raise ConfigError("Invalid value for '" + key + "'. Expecting datatype '" +
                                      datatype.__name__ + "'")
                except ConfigError as e:
                    raise ConfigError(key + " value not changed : " + e.message)

    def validate(self, key, value):
        if key == OBSTACLE_DISTANCE:
            if not 2 <= value <= 400:
                raise ConfigError("Obstacle Distance should range between 2-400")
        elif key == MOTOR_TURN_SPEED or key == MOTOR_SPEED:
            if not 0 <= value <= 100:
                raise ConfigError("All speed values should be between 0-100")
        elif key == BOT_TURN_TIME or key == BOT_INTER_NODE_TIME:
            if value < 0:
                raise ConfigError("All time values should be positive floats")
        elif key == RADAR_SCALE:
            if value & (~value + 1) != value:
                raise ConfigError("Radar scale should be a power of 2")
        elif key == RASPBERRY_IP:
            pattern = re.compile("^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
            result = re.match(pattern, value)
            if result:
                for i in result.groups():
                    if not 0 <= int(i) <= 255:
                        raise ConfigError("Invalid IP address format (range=[0-255])")
            else:
                raise ConfigError("Invalid IP address format.")
        elif key == RASPBERRY_PORT:
            if not 1 < value <= 65535:
                raise ConfigError("Port should range=[1-65535]")


class ConfigError(Exception):
    """
    Raised when config values entered by user are invalid.
    """


class ClientCameraHandler:
    """
    ClientCameraHandler class contains methods to perform operations on images taken by the raspberry pi camera
    """

    @staticmethod
    def convert_bytes_to_image(image_bytes, child, image_index):
        # image = image_bytes
        file_path = 'C:\\Users\\Niharika\\Desktop\\rasp pi project\\TarsImages\\'
        image_name = file_path + str(child[0]) + '_' + str(child[1]) + '_' + IMAGES_SEQUENCE[image_index] + ".jpg"
        new_image_file = open(image_name, 'wb')
        new_image_file.write(image_bytes)
        new_image_file.close()

    @staticmethod
    def convert_images_to_gif(shortest_path):
        pathname = 'C:\\Users\\Niharika\\Desktop\\rasp pi project\\TarsImages\\'
        images = []
        for node in shortest_path:
            image_name = pathname + str(node[0]) + '_' + str(node[1]) + "_middle_pic.jpg"
            image = Image.open(image_name)
            images.append(image)
        # file_names = [f for f in os.listdir(pathname) if f.endswith('.jpg')]
        # file_names = [(pathname+fn) for fn in file_names]
        # images = [Image.open(fn) for fn in file_names]
        size = (300, 300)
        for im in images:
            im.thumbnail(size, Image.ANTIALIAS)
        filename = pathname + "shortest_path.GIF"
        writeGif(filename, images, duration=0.2, dither=0)
