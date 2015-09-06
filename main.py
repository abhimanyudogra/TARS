from menus import MainMenu
from astar import *
import pygame
from radar import *
from constants import *
from pygame.locals import FULLSCREEN, DOUBLEBUF

cfg = {
    "speed": 65,
    "obstacle_distance": 10,
    "destination_x": 4,
    "destination_y": 4
}


class Display:
    def __init__(self, width, height):
        pygame.init()
        self.window = pygame.display.set_mode((width, height), DOUBLEBUF)
        pygame.display.set_caption("T.A.R.S")


class TARS:
    def __init__(self, config):
        self.config = config
        self.display = Display(WINDOW_X, WINDOW_Y)
        self.menus = MainMenu(self.display, config)
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            selection = self.menus.render_main()
            if selection == "Configure":
                modifications = self.menus.render_config()
                for (name, value) in modifications:
                    if value:
                        self.config.__dict__[name] = int(value)
            elif selection == "Deploy":
                self.radar = Radar(self.config, self.display)
                self.astar = AStar(self.config, self.radar)
                self.astar.run()
            elif selection == "Exit":
                self.exit_flag = True


class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    TARS(Config(**cfg)).run()
