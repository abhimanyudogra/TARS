#!/usr/bin/env python2.7

__author__ = "Niharika Dutta and Abhimanyu Dogra"

from pygame.locals import DOUBLEBUF

from TARS.client.menu.menus import *
from TARS.client.brain.astar import *
from TARS.client.radar.radar import *
from TARS.client.body.tars import *
from TARS.client.csocket.client_socket import *

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
    "raspberry_pi_address": "127.0.0.1",
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


class Controller:
    """
    Controller class drives the execution of the client side of TARS software
    """

    def __init__(self, config):
        self.config = config
        self.display = Display(config.window_width, config.window_height)
        self.menus = MainMenu(self.display, config)
        self.exit_flag = False
        self.client_socket = ClientSocket(self.config)
        self.tars = TARS(config, self.client_socket)

    def run(self):
        connected = False
        result = False
        while not self.exit_flag:
            selection = self.menus.render_main(connected, result)
            if selection == "Connect":
                while not connected:
                    try:
                        self.client_socket.connect()
                        connected = True
                    except socket.error:
                        try_again = self.menus.render_connect(self.config.raspberry_pi_address)
                        if not try_again:
                            break
            elif selection == "Disconnect":
                self.client_socket.close()
                connected = False
            elif selection == "Configure":
                field_names, field_values = self.menus.render_config()
                if field_values:
                    for (name, value) in zip(field_names, field_values):
                        if value:
                            for (datatype, pool) in datatypes.items():
                                key = name.replace(" ", "_").lower()
                                if key in pool:
                                    print "MAIN : Updating " + str(key) + " to " + value
                                    self.config.__dict__[key] = datatype(value)
            elif selection == "Deploy":
                self.display.run()
                radar = Radar(self.config, self.display)
                self.tars.set_radar(radar)
                astar = AStar(self.config, radar, self.tars)
                result = astar.run()
                print "RESULT :::::::::::: " + result
            elif selection == "Exit":
                self.display.shutdown()
                self.exit_flag = True
        self.client_socket.close()


class Config(object):
    """
    Config class stores all configurable variables.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == "__main__":
    Controller(Config(**cfg)).run()
