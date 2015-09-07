from constants import *


class DirectionHandler:

    @staticmethod
    def turn_cw(direction):
        idx = DIRECTIONS.index(direction)
        if idx == 3:
            return DIRECTIONS[0]
        else:
            return DIRECTIONS[idx + 1]

    @staticmethod
    def turn_acw(direction):
        idx = DIRECTIONS.index(direction)
        if idx == 0:
            return DIRECTIONS[3]
        else:
            return DIRECTIONS[idx - 1]
