#!/usr/bin/env python2.7

__author__ = "Niharika Dutta and Abhimanyu Dogra"

from pygame.locals import DOUBLEBUF
from client.menu.menus import *
from client.brain.astar import *
from client.radar.radar import *
from client.body.tars import *
from client.csocket.client_socket import *

cfg = {
    "obstacle_distance": 10,  # Distance for which TARS considers next node or obstacles.
    "destination_x": 4,  # X co-ordinate of destination
    "destination_y": 4,  # Y co-ordinate of destination
    "motor_speed": 65,  # speed = pwm duty cycle, 0 = off, 100 = max
    "motor_turn_time": 0.4,
    "motor_turn_speed": 65,  # speed = pwm duty cycle, 0 = off, 100 = max
    "motor_node_travel_time": 2,
    "window_width": 1280,
    "window_height": 768,
    "radar_scale": 8,
    "raspberry_pi_address": "192.168.1.6",
    "raspberry_pi_port": 5000
}

datatypes = {
    int: {"destination_x", "destination_y", "motor_speed", "motor_turn_speed", "window_width", "window_height",
          "radar_scale", "raspberry_pi_port"},
    float: {"obstacle_distance", "motor_turn_time", "motor_node_travel_time"},
    str: {"raspberry_pi_ip", }
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


class ProgramState:
    """
    Class responsible for tracking the current state of the client application
    """

    def __init__(self):
        self.connection = None
        self.result = None
        self.selection = None
        self.exit = False

    def toggle_exit(self):
        self.exit = not self.exit


class Controller:
    """
    Controller class drives the execution of the client side of TARS software
    """

    def __init__(self, config):
        self.state = ProgramState()
        self.config = config
        self.display = Display(config.window_width, config.window_height)
        self.menus = MainMenu(self.display, config, self.state)
        self.client_socket = ClientSocket(self.config)
        self.tars = TARS(config, self.client_socket)

    def run(self):
        while not self.state.exit:
            self.state.selection = self.menus.render_main()
            if self.state.selection in {RETRY, RECONNECT, CONNECT}:
                while not self.state.connection == CONNECTED:
                    self.state.connection = self.client_socket.connect()
                    if self.state.connection in {TIMEOUT, CONNECTION_ERROR}:
                        try_again = self.menus.render_connect()
                        if not try_again:
                            break
            elif self.state.selection == DISCONNECT:
                self.client_socket.close()
                self.state.connection = UNCONNECTED
            elif self.state.selection == SETTINGS:
                field_names, field_values = self.menus.render_config()
                if field_values:
                    for (name, value) in zip(field_names, field_values):
                        if value:
                            for (datatype, pool) in datatypes.items():
                                key = name.replace(" ", "_").lower()
                                if key in pool:
                                    print "MAIN : Updating " + str(key) + " to " + value
                                    self.config.__dict__[key] = datatype(value)
            elif self.state.selection == DEPLOY:
                self.display.run()
                radar = Radar(self.config, self.display)
                self.tars.set_radar(radar)
                astar = AStar(self.config, radar, self.tars)
                self.state.result = astar.run()
            elif self.state.selection == "Exit":
                self.state.exit = True
        self.display.shutdown()
        if self.state.connection == CONNECTED:
            self.client_socket.close()


class Config(object):
    """
    Config class stores all configurable variables.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    Controller(Config(**cfg)).run()
