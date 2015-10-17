#!/usr/bin/env python
__author__ = "Niharika Dutta and Abhimanyu Dogra"

import re
import sys

from server_socket import ServerSocket
from server_constants import *
from gpio_handler import GPIOHandler
from camera_handler import ServerCameraHandler



# Regex pattern for extracting co-ordinates from string representation of a tuple
DIRECTION_TUPLE_PATTERN = re.compile("\((\d+), (\d+)\)")


class Controller:
    """
    Drives the server side of TARS application. Controls the signals through GPIO pins based on the messages received
    from the client connection.
    """

    def __init__(self):
        self.soc = ServerSocket()
        self.gpio_handler = GPIOHandler()
        self.camera = ServerCameraHandler()

    def parse_message(self, msg):
        content = msg.split("|")
        result = re.match(DIRECTION_TUPLE_PATTERN, content[1])
        direction = list(result.groups())
        for i in xrange(0, len(direction)):
            direction[i] = int(direction[i])
        settings = (tuple(direction), int(content[2]))
        return settings

    def run(self):
        try:
            while True:
                msg = self.soc.listen()
                if msg == STARTUP:
                    print "startup"
                    self.gpio_handler.startup()
                elif msg.startswith(MOTOR_CHANGE):
                    settings = self.parse_message(msg)
                    self.gpio_handler.motor_change(settings)
                elif msg == DETECT_OBSTACLE:
                    self.soc.reply("@" + str(self.gpio_handler.detect_obstacle()))
                elif msg == CLICK_PICTURE:
                    self.soc.reply(str(self.camera.click_picture()))
                elif msg in {STANDBY, SOCKET_ERROR}:
                    self.soc.standby()
        except KeyboardInterrupt:
            self.soc.shutdown()
            self.gpio_handler.shutdown()
            sys.exit()


if __name__ == "__main__":
    Controller().run()
