import pygame
import time
import random
from constants import *
from pygame.locals import FULLSCREEN, DOUBLEBUF

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (120, 0, 0)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 90, 0)
YELLOW = (255,255,0)

class Bot:
    def __init__(self):
        self.position = (OFFSET_X, OFFSET_Y)
        self.color = RED
        self.size = OBJECT_SIZE

    def update(self, position):
        self.position = position

    def render(self, window):
        pygame.draw.rect(window, self.color,
                         (self.position[0] + OFFSET_OBJECT + 1, self.position[1] + OFFSET_OBJECT + 1,
                          self.size - 1, self.size - 1))


class Walls:
    positions = []

    def __init__(self):
        self.color = DARK_GREEN
        self.size = SCALE + 1

    def add_wall(self, position):
        self.positions.append(position)

    def render(self, window):
        for position in self.positions:
            pygame.draw.rect(window, self.color,
                             (position[0], position[1],
                              self.size, self.size))


class Destination:
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
    def __init__(self, config, display):
        self.dest_orig = (config.destination_x,config.destination_y)
        self.destination = Destination(self.convert((config.destination_x,config.destination_y)))
        self.bot = Bot()
        self.bot_orig = (0, 0)
        self.walls = Walls()
        self.window = display.window
        self.shortest_path = []

    def convert(self, coordinates):
        return coordinates[0] * SCALE + OFFSET_X, OFFSET_Y - coordinates[1] * SCALE

    def update(self, object, location):
        if object == BOT:
            self.bot_orig = location
            self.bot.update(self.convert(location))
        elif object == WALL:
            self.walls.add_wall(self.convert(location))
        elif object == SHORTEST_PATH:
            self.shortest_path = location

    def render(self):
        self.window.fill(BLACK)
        for i in xrange(128):
            pygame.draw.line(self.window, DARK_GREEN, (i * SCALE, 0), (i * SCALE, WINDOW_Y))

        for i in xrange(72):
            pygame.draw.line(self.window, DARK_GREEN, (0, i * SCALE), (WINDOW_X, i * SCALE))

        self.bot.render(self.window)
        self.walls.render(self.window)
        self.destination.render(self.window)
        if self.shortest_path:
            for node in self.shortest_path:
                node = self.convert(node)
                pygame.draw.rect(self.window, YELLOW,
                         (node[0], node[1] ,SCALE + 1,SCALE + 1))

        pygame.display.set_caption("Bot : %s, Destination : %s" % (str(self.bot_orig), str(self.dest_orig)))
        pygame.display.flip()



if __name__ == "__main__":
    radar = Radar((4, 4))
    radar.render()
    walls = ((1, 1), (2, 2), (3, 4), (-2, -2), (-2, 5), (2, -6))
    x, y = 0, 0
    for wall in walls:
        flag = random.randint(0, 1)
        radar.update(WALL, wall)
        if flag:
            x += 1
        else:
            y += 1
        radar.update(BOT, (x, y))
        radar.render()
        time.sleep(1)
    time.sleep(5)
