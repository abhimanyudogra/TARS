#!/usr/bin/env python2.7

__author__ = "Niharika Dutta and Abhimanyu Dogra"

from pygame.locals import DOUBLEBUF

from client.menu.menus import *
from client.brain.astar import *
from client.radar.radar import *
from client.body.bot import *
from client.csocket.client_socket import *
from client.utility.utilities import *

cfg = {
    OBSTACLE_DISTANCE: 10,  # Distance for which TARS considers next node or obstacles.
    DESTINATION_X: 4,  # X co-ordinate of destination
    DESTINATION_Y: 4,  # Y co-ordinate of destination
    MOTOR_SPEED: 65,  # speed = pwm duty cycle, 0 = off, 100 = max
    BOT_TURN_TIME: 0.4,
    MOTOR_TURN_SPEED: 65,  # speed = pwm duty cycle, 0 = off, 100 = max
    BOT_INTER_NODE_TIME: 2,
    WINDOW_WIDTH: 1280,
    WINDOW_HEIGHT: 768,
    RADAR_SCALE: 8,
    RASPBERRY_IP: "127.0.0.1",
    RASPBERRY_PORT: 5000
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

    def state(self):
        if not self.result and not self.connection:
            return ALPHA
        elif self.connection == TIMEOUT:
            return BETA
        elif self.connection == CONNECTION_ERROR:
            return GAMMA
        elif self.connection == UNCONNECTED:
            return DELTA
        elif self.connection == CONNECTED and not self.result:
            return EPSILON
        elif self.connection == CONNECTED and self.result == DESTINATION_BLOCKED:
            return ZETA
        elif self.connection == CONNECTED and self.result == DESTINATION_UNREACHABLE:
            return ETA
        elif self.connection == CONNECTED and self.result == MANUAL_EXIT:
            return THETA
        elif self.connection == CONNECTED and self.result == DESTINATION_FOUND:
            return IOTA


class Controller:
    """
    Controller class drives the execution of the client side of TARS software
    """

    def __init__(self, config):
        self.state = ProgramState()
        self.config = config
        self.display = Display(config[WINDOW_WIDTH], config[WINDOW_HEIGHT])
        self.menus = MainMenu(self.display, self.config, self.state)
        self.client_socket = ClientSocket(self.config)
        self.bot = Bot(config, self.client_socket)

    def run(self):
        while not self.state.exit:
            self.state.selection = self.menus.render_main()
            self.menus.clear_notifications()
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
                self.state.result = None
            elif self.state.selection == SETTINGS:
                field_names, field_values = self.menus.render_config()
                if field_values:
                    self.update_config(field_names, field_values)
            elif self.state.selection == DEPLOY:
                self.display.run()
                radar = Radar(self.config, self.display)
                self.bot.set_radar(radar)
                astar = AStar(self.config, radar, self.bot)
                self.state.result = astar.run()
            elif self.state.selection == EXIT:
                self.state.exit = True
        self.display.shutdown()
        if self.state.connection == CONNECTED:
            self.client_socket.close()

    def update_config(self, field_names, field_values):
        for (key, value) in zip(field_names, field_values):
            if value:
                try:
                    self.config[key] = value
                except ConfigError as e:
                    self.menus.notify(e.message)


if __name__ == "__main__":
    Controller(Config(**cfg)).run()
