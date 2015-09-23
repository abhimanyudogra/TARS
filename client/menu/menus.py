__author__ = "Niharika Dutta and Abhimanyu Dogra"

import easygui

from TARS.client.utility.client_constants import *


class MainMenu:
    """
    MainMenu class handles the rendering of all the menus for the software.
    """

    def __init__(self, window, config):
        self.window = window
        self.config = config

    def render_main(self, connected, last_result):
        msg = ""
        if not last_result:
            msg = "Greetings human.\nYou can configure my settings in 'Configure' menu.\nOnce connected to server, press" \
                  "'Deploy' to run the algorithm."
        elif last_result == DESTINATION_UNREACHABLE:
            msg = "Uh oh.I traversed all reachable nodes but the destination seems to be out of coverage."
        elif last_result == DESTINATION_BLOCKED:
            msg = "The destination is blocked on all sides."
        elif last_result == MANUAL_EXIT:
            msg = "Algorithm was manually stopped."
        elif last_result == DESTINATION_FOUND:
            msg = "Destination reached."
        title = "T.A.R.S main terminal"
        buttons = ["Configure", "Exit"]
        if not connected:
            buttons.insert(0, "Connect")
        else:
            buttons.insert(0, "Disconnect")
            buttons.insert(1, "Deploy")
            title += " (Connected)"
        selection = easygui.buttonbox(msg, title, buttons)
        return selection

    def render_config(self):
        field_names = [setting.replace("_", " ").title() for setting in sorted(self.config.__dict__.keys())]
        msg = "Modify T.A.R.S settings."
        title = "Configure T.A.R.S"
        field_values = easygui.multenterbox(msg, title, field_names)
        return field_names, field_values

    def render_connect(self, ip):
        msg = "Unable to connect."
        title = "Connecting to " + ip
        buttons = ["Retry", "Cancel"]
        selection = easygui.buttonbox(msg, title, buttons)
        return selection == "Retry"
