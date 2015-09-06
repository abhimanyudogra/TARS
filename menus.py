import easygui


class MainMenu:
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
        fieldNames = [setting for setting in self.config.__dict__.keys()]
        fieldValues = []
        msg = "Modify T.A.R.S settings."
        title = "Configure T.A.R.S"
        fieldValues = easygui.multenterbox(msg, title, fieldNames)
        return zip(fieldNames, fieldValues)
