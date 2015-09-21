from server_handler import ServerSocket
from server_constants import *
from gpio_handler import GPIOHandler
import re
import sys

DIRECTION_TUPLE_PATTERN = re.compile("\((\d+), (\d+)\)")


class Controller:
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
                    self.gpio_handler.startup()
                elif msg.startswith(MOTOR_CHANGE):
                    direction = self.parse_direction(msg)
                    self.gpio_handler.motor_change(direction)
                elif msg == DETECT_OBSTACLE:
                    self.socket.reply(str(self.gpio_handler.detect_obstacle()))
        except KeyboardInterrupt:
            self.socket.shutdown()
            self.gpio_handler.shutdown()
            sys.exit()


if __name__ == "__main__":
    Controller().run()
    print "LULZ"
