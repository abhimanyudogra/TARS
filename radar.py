import pygame
from constants import *

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
    """

    def __init__(self):
        self.color = BLUE
        self.size = SCALE
        self.positions = []

    def add(self, position):
        self.positions.append(position)

    def render(self, window):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0] + 1, position[1] + 1, self.size - 1, self.size - 1))

    def reset(self):
        self.positions = []


class ShortestPath:
    """
    ShortestPath class stores information about all the nodes that form the shortest path as a result of the search
    algorithm.
    """

    def __init__(self):
        self.path = []
        self.color = YELLOW
        self.size = OBJECT_SIZE - 1

    def set_path(self, path):
        self.path = path

    def render(self, window):
        for node in self.path:
            pygame.draw.rect(window, self.color,
                             (node[0] + OFFSET_OBJECT + 1, node[1] + OFFSET_OBJECT + 1, self.size, self.size))


class Trail:
    """
    Trail stores the information about all the nodes visited by the bot.
    """

    def __init__(self):
        self.color = DARK_BLUE
        self.size = SCALE
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

    def __init__(self):
        self.position = (OFFSET_X, OFFSET_Y)
        self.color = RED
        self.size = OBJECT_SIZE - 1

    def update(self, position):
        self.position = position

    def render(self, window):
        pygame.draw.rect(window, self.color,
                         (self.position[0] + OFFSET_OBJECT + 1, self.position[1] + OFFSET_OBJECT + 1,
                          self.size, self.size))

    def reset(self):
        self.position = (OFFSET_X, OFFSET_Y)


class Walls:
    """
    Walls class stores information about all the nodes acting as a wall.
    """

    def __init__(self):
        self.color = DARK_GREEN
        self.size = SCALE + 1
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

    def __init__(self, position):
        self.position = position
        self.color = BLUE
        self.size = OBJECT_SIZE

    def update(self, position):
        self.position = position

    def render(self, window):
        pygame.draw.rect(window, self.color,
                         (self.position[0] + OFFSET_OBJECT + 1, self.position[1] + OFFSET_OBJECT + 1,
                          self.size - 1, self.size - 1))


class Radar:
    """
    Radar class handles the visual display the the searching process.
    """

    def __init__(self, config, display):
        self.dest_orig = (config.destination_x, config.destination_y)
        self.destination = Destination(self.convert((config.destination_x, config.destination_y)))
        self.bot = Bot()
        self.bot_orig = (0, 0)
        self.walls = Walls()
        self.window = display.window
        self.trail = Trail()
        self.shortest_path = ShortestPath()
        self.highlights = Highlights()

    def convert(self, coordinates):
        return coordinates[0] * SCALE + OFFSET_X, OFFSET_Y - coordinates[1] * SCALE

    def update(self, object, location):
        if object == BOT:
            self.bot_orig = location
            self.trail.add(self.bot.position)
            self.bot.update(self.convert(location))
        elif object == WALL:
            self.walls.add(self.convert(location))
        elif object == SHORTEST_PATH:
            self.shortest_path.set_path([self.convert(node) for node in location])
        elif object == HIGHLIGHT:
            self.highlights.add(self.convert(location))
        self.render()

    def render(self):
        pygame.event.pump()
        self.window.fill(BLACK)
        for i in xrange(1000):
            pygame.draw.line(self.window, DARK_GREEN, (i * SCALE, 0), (i * SCALE, WINDOW_Y))

        for i in xrange(500):
            pygame.draw.line(self.window, DARK_GREEN, (0, i * SCALE), (WINDOW_X, i * SCALE))

        self.walls.render(self.window)
        self.trail.render(self.window)
        if self.shortest_path.path:
            self.shortest_path.render(self.window)
        self.destination.render(self.window)
        self.bot.render(self.window)

        pygame.display.set_caption("Bot : %s, Destination : %s" % (str(self.bot_orig), str(self.dest_orig)))
        pygame.display.flip()
