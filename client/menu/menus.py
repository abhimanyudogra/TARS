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

    def render_main(self):
        msg = "Greetings human.\nYou can configure my settings in 'Configure' menu.\nPress 'Connect' button for " \
              "connecting to the Raspberry Pi.\nMake sure you have configured the right IP address and port."
        title = "T.A.R.S main terminal"
        buttons = [DISCONNECT, DEPLOY, SETTINGS, EXIT]

        if not self.state.result and not self.state.connection:
            buttons = [CONNECT, SETTINGS, EXIT]
        elif self.state.connection == TIMEOUT:
            msg = "TARS did not respond and connection request timed out. " \
                  "Ensure he is on network and try connecting again."
            buttons = [RETRY, SETTINGS, EXIT]
        elif self.state.connection == CONNECTION_ERROR:
            msg = "There was an error while communicating with TARS."
            buttons = [RETRY, SETTINGS, EXIT]
        elif self.state.connection == UNCONNECTED:
            msg = "Disconnected from TARS."
            buttons = [RECONNECT, SETTINGS, EXIT]
        elif self.state.connection == CONNECTED and not self.state.result:
            msg = "Great! Now press 'Deploy' to run the search algorithm."
        elif self.state.connection == CONNECTED and self.state.result == DESTINATION_BLOCKED:
            msg = "The destination is blocked on all four sides."
        elif self.state.connection == CONNECTED and self.state.result == DESTINATION_UNREACHABLE:
            msg = "Uh oh.I traversed all reachable nodes but the destination seems to be out of coverage."
        elif self.state.connection == CONNECTED and self.state.result == MANUAL_EXIT:
            msg = "Algorithm was manually stopped. How will you like to proceed?"
        elif self.state.connection == CONNECTED and self.state.result == DESTINATION_FOUND:
            msg = "Eureka! destination reached. "

        selection = easygui.buttonbox(msg, title, buttons)
        return selection

    def render_config(self):
        field_names = [setting.replace("_", " ").title() for setting in sorted(self.config.__dict__.keys())]
        msg = "Modify T.A.R.S settings."
        title = "Configure T.A.R.S"
        field_values = easygui.multenterbox(msg, title, field_names)
        return field_names, field_values

    def render_connect(self):
        title = "Error while connecting to " + self.config.raspberry_pi_address
        buttons = [RETRY, CANCEL]
        msg = ""
        if self.state.connection == TIMEOUT:
            msg = "Server did not respond. This may be due to some other connection keeping it busy."
        elif self.state.connection == CONNECTION_ERROR:
            msg = "There was a socket error while connecting to TARS."
        selection = easygui.buttonbox(msg, title, buttons)
        return selection == RETRY
