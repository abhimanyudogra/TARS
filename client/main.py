#!/usr/bin/env python

__author__ = "Niharika Dutta and Abhimanyu Dogra"

from pygame.locals import DOUBLEBUF

from TARS.client.menu.menus import MainMenu
from TARS.client.brain.astar import *
from TARS.client.radar.radar import *
from TARS.client.body.tars import *
from TARS.client.csocket.client_socket import *

cfg = {
    "speed": 65,  # Movement speed
    "obstacle_distance": 10,  # Distance for which TARS considers next node or obstacles.
    "destination_x": 4,  # X co-ordinate of destination
    "destination_y": 4  # Y co-ordinate of destination
}


class Display:
    """
    Display class wraps the pygame window which is used to display the radar etc.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = None

    def run(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
        pygame.display.set_caption("T.A.R.S")

    def shutdown(self):
        pygame.display.quit()
        pygame.quit()


class Controller:
    """
    Controller class drives the execution of the client side of TARS software
    """

    def __init__(self, config):
        self.config = config
        self.display = Display(WINDOW_X, WINDOW_Y)
        self.menus = MainMenu(self.display, config)
        self.exit_flag = False
        self.client_socket = ClientSocket()
        self.tars = TARS(config, self.client_socket)

    def run(self):
        while not self.exit_flag:
            selection = self.menus.render_main()
            if selection == "Configure":
                field_names, field_values = self.menus.render_config()
                if field_values:
                    for (name, value) in zip(field_names, field_values):
                        if value:
                            self.config.__dict__[name] = int(value)
            elif selection == "Deploy":
                self.display.run()
                radar = Radar(self.config, self.display)
                astar = AStar(self.config, radar, self.tars)
                astar.run()
            elif selection == "Exit":
                self.display.shutdown()
                self.exit_flag = True
        self.client_socket.send(STANDBY)
        self.client_socket.close()


class Config(object):
    """
    Config class stores all configurable variables.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    Controller(Config(**cfg)).run()
