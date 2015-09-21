#!/usr/bin/env python
__author__ = "Niharika Dutta and Abhimanyu Dogra"

import re
import sys

from server_handler import ServerSocket
from server_constants import *
from gpio_handler import GPIOHandler


# Regex pattern for extracting co-ordinates from string representation of a tuple
DIRECTION_TUPLE_PATTERN = re.compile("\((\d+), (\d+)\)")


class Controller:
    """
    Drives the server side of TARS application. Controls the signals through GPIO pins based on the messages received
    from the client connection.
    """

    def __init__(self):
        self.socket = ServerSocket()
        self.gpio_handler = GPIOHandler(BOT_SPEED)

    def parse_direction(self, msg):
        msg = msg.replace(MOTOR_CHANGE, "")
        result = re.match(DIRECTION_TUPLE_PATTERN, msg)
        direction = list(result.groups())
        for i in xrange(0, len(direction)):
            direction[i] = int(direction[i])
        return tuple(direction)

    def run(self):
        try:
            while True:
                msg = self.socket.listen()
                if msg == STARTUP:
                    pass
                    self.gpio_handler.startup()
                elif msg.startswith(MOTOR_CHANGE):
                    direction = self.parse_direction(msg)
                    self.gpio_handler.motor_change(direction)
                elif msg == DETECT_OBSTACLE:
                    pass
                    self.socket.reply("False")
                    self.socket.reply(str(self.gpio_handler.detect_obstacle()))
        except KeyboardInterrupt:
            self.socket.shutdown()
            self.gpio_handler.shutdown()
            sys.exit()


if __name__ == "__main__":
    Controller().run()
