__author__ = "Niharika Dutta and Abhimanyu Dogra"

import pygame

from TARS.client.utility.client_constants import *

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 90, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 75)


class Highlights:
    """
    Highlight class stores information about all the nodes required to be highlighted.
    For example, AStar highlights each child node that is being considered.
    """

    def __init__(self, config):
        self.color = BLUE
        self.size = config["scale"]
        self.positions = []

    def add(self, position):
        self.positions.append(position)

    def render(self, window):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0], position[1] + 1, self.size, self.size - 1))

    def reset(self):
        self.positions = []


class ShortestPath:
    """
    ShortestPath class stores information about all the nodes that form the shortest path as a result of the search
    algorithm.
    """

    def __init__(self, config):
        self.config = config
        self.path = []
        self.color = YELLOW
        self.size = config["object_size"] - 1

    def set_path(self, path):
        self.path = path

    def render(self, window):
        for node in self.path:
            pygame.draw.rect(window, self.color, (node[0] + self.config["offset_object"] + 1, node[1] +
                                                  self.config["offset_object"] + 1, self.size, self.size))


class Trail:
    """
    Trail stores the information about all the nodes visited by the bot.
    """

    def __init__(self, config):
        self.color = DARK_BLUE
        self.size = config["scale"]
        self.positions = []

    def add(self, position):
        self.positions.append(position)

    def render(self, window):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0] + 1, position[1] + 1, self.size - 1, self.size - 1))

    def reset(self):
        self.positions = []


class Bot:
    """
    Bot class stores information about the object representing the current position of the bot.
    """

    def __init__(self, config):
        self.config = config
        self.position = (config["offset_x"], config["offset_y"])
        self.color = RED
        self.size = config["object_size"] - 1

    def update(self, position):
        self.position = position

    def render(self, window):
        pygame.draw.rect(window, self.color,
                         (self.position[0] + self.config["offset_object"] + 1, self.position[1] +
                          self.config["offset_object"] + 1, self.size, self.size))

    def reset(self):
        self.position = (self.config["offset_x"], self.config["offset_y"])


class Walls:
    """
    Walls class stores information about all the nodes acting as a wall.
    """

    def __init__(self, config):
        self.color = DARK_GREEN
        self.size = config["scale"] + 1
        self.positions = []

    def add(self, position):
        self.positions.append(position)

    def render(self, window):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0], position[1], self.size, self.size))

    def reset(self):
        self.positions = []


class Destination:
    """
    Destination class represents the node acting as the destination for the bot.
    """

    def __init__(self, config):
        self.config = config
        self.position = config["destination"]
        self.color = BLUE
        self.size = config["object_size"]

    def update(self, position):
        self.position = position

    def render(self, window):
        pygame.draw.rect(window, self.color,
                         (self.position[0] + self.config["offset_object"] + 1, self.position[1] +
                          self.config["offset_object"] + 1, self.size - 1, self.size - 1))


class Radar:
    """
    Radar class handles the visual display the the searching process.
    """

    def __init__(self, config, display):
        self.config = dict()
        self.window_x = config.window_width
        self.window_y = config.window_height
        self.config["scale"] = config.radar_scale
        self.config["offset_x"] = config.window_width / 2
        self.config["offset_y"] = config.window_height / 2
        self.config["destination"] = self.convert((config.destination_x, config.destination_y))
        self.config["object_size"] = config.radar_scale / 2
        self.config["offset_object"] = self.config["scale"] / 2 - self.config["object_size"] / 2

        self.destination = Destination(self.config)
        self.bot = Bot(self.config)
        self.walls = Walls(self.config)
        self.window = display.window
        self.trail = Trail(self.config)
        self.shortest_path = ShortestPath(self.config)
        self.highlights = Highlights(self.config)

    def convert(self, coordinates):
        return coordinates[0] * self.config["scale"] + self.config["offset_x"], \
               self.config["offset_y"] - coordinates[1] * self.config["scale"]

    def update(self, obj, location):
        if obj == BOT:
            self.trail.add(self.bot.position)
            self.bot.update(self.convert(location))
        elif obj == WALL:
            self.walls.add(self.convert(location))
        elif obj == SHORTEST_PATH:
            self.shortest_path.set_path([self.convert(node) for node in location])
        elif obj == HIGHLIGHT:
            self.highlights.add(self.convert(location))
        self.render()

    def render(self):
        pygame.event.pump()
        self.window.fill(BLACK)
        for i in xrange(1000):
            pygame.draw.line(self.window, DARK_GREEN, (i * self.config["scale"], 0), (i * self.config["scale"],
                                                                                      self.window_y))

        for i in xrange(500):
            pygame.draw.line(self.window, DARK_GREEN, (0, i * self.config["scale"]), (self.window_x,
                                                                                      i * self.config["scale"]))

        self.walls.render(self.window)
        self.trail.render(self.window)
        self.highlights.render(self.window)
        if self.shortest_path.path:
            self.shortest_path.render(self.window)
        self.destination.render(self.window)
        self.bot.render(self.window)

        pygame.display.set_caption("Bot : %s, Dest : %s" % (str(self.bot.position), str(self.destination.position)))
        pygame.display.flip()
