__author__ = "Niharika Dutta and Abhimanyu Dogra"

import easygui

from client.utility.client_constants import *


class MainMenu:
    """
    MainMenu class handles the rendering of all the menus for the software.
    """

    def __init__(self, window, config, state):
        self.window = window
        self.config = config
        self.state = state
        self.notifications = []
        self.field_name_map = {
            OBSTACLE_DISTANCE: "Obstacle distance (integer, range=[2, 400])",
            DESTINATION_X: "Destination x coordinate (integer)",
            DESTINATION_Y: "Destination y coordinate (integer)",
            MOTOR_SPEED: "Motor speed (integer, range [0-100]",
            BOT_TURN_TIME: "TARS turn time (seconds, default=0.5)",
            MOTOR_TURN_SPEED: "Motor turn speed (integer, range=[0-100])",
            BOT_INTER_NODE_TIME: "TARS inter-node travel time (seconds, 2)",
            WINDOW_WIDTH: "Width of radar window (integer, 2^n)",
            WINDOW_HEIGHT: "Height of radar window (integer, 2^n)",
            RADAR_SCALE: "Radar scale (integer, 2^n)",
            RASPBERRY_IP: "TARS IP address (default : 127.0.0.1)",
            RASPBERRY_PORT: "TARS port (default : 5000)",
        }

    def render_main(self):
        msg = "Greetings human.\nYou can configure my settings in 'Configure' menu.\nPress 'Connect' button for " \
              "connecting to the Raspberry Pi.\nMake sure you have configured the right IP address and port."
        title = "T.A.R.S main terminal"
        buttons = [DISCONNECT, DEPLOY, SETTINGS, EXIT]
        current_state = self.state.state()
        if current_state == ALPHA:
            buttons = [CONNECT, SETTINGS, EXIT]
        elif current_state == BETA:
            msg = "TARS did not respond and connection request timed out. " \
                  "Ensure he is on network and try connecting again."
            buttons = [RETRY, SETTINGS, EXIT]
        elif current_state == GAMMA:
            msg = "There was an error while communicating with TARS."
            buttons = [RETRY, SETTINGS, EXIT]
        elif current_state == DELTA:
            msg = "Disconnected from TARS."
            buttons = [RECONNECT, SETTINGS, EXIT]
        elif current_state == EPSILON:
            msg = "Great! Now press 'Deploy' to run the search algorithm."
        elif current_state == ZETA:
            msg = "The destination is blocked on all four sides."
        elif current_state == ETA:
            msg = "Uh oh.I traversed all reachable nodes but the destination seems to be out of coverage."
        elif current_state == THETA:
            msg = "Algorithm was manually stopped. How will you like to proceed?"
        elif current_state == IOTA:
            msg = "Eureka! destination reached. "

        for notification in self.notifications:
            msg += "\n_____________________"
            msg += "\nAlert! : " + notification
        selection = easygui.buttonbox(msg, title, buttons)
        return selection

    def render_config(self):
        field_names = [setting for setting in sorted(self.config.__dict__.keys())]
        field_desc = [self.field_name_map[key] for key in field_names]
        msg = "Modify T.A.R.S settings."
        title = "Configure T.A.R.S"
        field_values = easygui.multenterbox(msg, title, field_desc)
        return field_names, field_values

    def render_connect(self):
        title = "Error while connecting to " + self.config[RASPBERRY_IP]
        buttons = [RETRY, CANCEL]
        msg = ""
        if self.state.connection == TIMEOUT:
            msg = "Server did not respond. This may be due to some other connection keeping it busy."
        elif self.state.connection == CONNECTION_ERROR:
            msg = "There was a socket error while connecting to TARS."
        selection = easygui.buttonbox(msg, title, buttons)
        return selection == RETRY

    def notify(self, msg):
        self.notifications.append(msg)

    def clear_notifications(self):
        self.notifications = []
