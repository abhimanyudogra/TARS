__author__ = "Niharika Dutta and Abhimanyu Dogra"

import easygui


class MainMenu:
    """
    MainMenu class handles the rendering of all the menus for the software.
    """

    def __init__(self, window, cfg):
        self.window = window
        self.config = cfg

    def render_main(self):
        msg = "Greetings human."
        title = "T.A.R.S main terminal"
        buttons = ["Configure", "Deploy", "Exit"]
        selection = easygui.buttonbox(msg, title, buttons)
        return selection

    def render_config(self):
        field_names = [setting for setting in self.config.__dict__.keys()]
        msg = "Modify T.A.R.S settings."
        title = "Configure T.A.R.S"
        field_values = easygui.multenterbox(msg, title, field_names)
        return field_names, field_values
