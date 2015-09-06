from menus import MainMenu
from astar import AStar
import pygame
from pygame.locals import FULLSCREEN, DOUBLEBUF

cfg = {
    "speed": 65,
    "obstacle_distance": 10,
    "window_x": 768,
    "window_y": 768,
    "destination_x" : 0,
    "destination_y" : 0
}


class Display:
    def __init__(self, width, height):
        pygame.init()
        self.window = pygame.display.set_mode((width, height), DOUBLEBUF)
        pygame.display.set_caption("T.A.R.S")


class TARS:
    def __init__(self, config):
        self.config = config
        self.display = Display(config.window_x, config.window_y)
        self.menus = MainMenu(self.display, config)
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            selection = self.menus.render_main()
            if selection == "Configure":
                modifications = self.menus.render_config()
                for (name,value) in modifications:
                    if isinstance(value,(int)):
                        self.config.__dict__[name] = int(value)

            elif selection == "Deploy":
                self.astar = AStar(self.config)
                self.astar.run()

class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    TARS(Config(**cfg)).run()
