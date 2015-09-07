from copy import copy
import time
from gpio_handler import *
from constants import *
from utility import DirectionHandler


class TARS:
    def __init__(self, config, gpio_handler):
        self.motor_directions = STOP
        self.config = config
        self.gpio_handler = gpio_handler
        self.direction = NORTH

    def move_to_destination(self, curr_node, next_node):
        if next_node.parent != curr_node:
            print "backtracking..."
            common_ancestor = self.find_common_ancestor(curr_node, next_node)
            path_between = self.create_path(curr_node, next_node, common_ancestor)
            self.traverse_between(path_between)
        else:
            if next_node == curr_node.left:
                self.turn_left()
            if next_node == curr_node.right:
                self.turn_right()
            self.motor_directions = FORWARD
            self.move_to_node()

    def find_common_ancestor(self, curr_node, next_node):
        path = copy(curr_node.path)
        path.reverse()
        for node in path:
            if node in next_node.ancestors:
                return node

    def traverse_between(self, path):
        self.turn_right()
        self.turn_right()
        index = 0
        self.motor_directions = FORWARD
        while index != len(path) - 1:
            curr = path[index]
            nxt = path[index + 1]
            if self.direction == NORTH:
                if nxt[0] < curr[0]:
                    self.turn_left()
                elif nxt[0] > curr[0]:
                    self.turn_right()
            elif self.direction == WEST:
                if nxt[1] < curr[1]:
                    self.turn_left()
                elif nxt[1] > curr[1]:
                    self.turn_right()
            elif self.direction == EAST:
                if nxt[1] < curr[1]:
                    self.turn_right()
                elif nxt[1] > curr[1]:
                    self.turn_left()
            else:
                if nxt[0] < curr[0]:
                    self.turn_right()
                elif nxt[0] > curr[0]:
                    self.turn_left()
            self.move_to_node()
            index += 1

    def create_path(self, curr_node, next_node, common_ancestor):
        common_ancestor_idx = curr_node.path.index(common_ancestor)
        subset = slice(common_ancestor_idx, len(curr_node.path))
        path1 = curr_node.path[subset]
        common_ancestor_idx = next_node.path.index(common_ancestor)
        subset = slice(common_ancestor_idx + 1, len(next_node.path))
        path2 = next_node.path[subset]
        path2.append((next_node.x, next_node.y))
        path1.reverse()
        path1.extend(path2)
        path1.insert(0, (curr_node.x, curr_node.y))
        return path1

    def turn_left(self):
        self.direction = DirectionHandler.turn_acw(self.direction)
        self.motor_directions = LEFT
        self.turn()

    def turn_right(self):
        self.direction = DirectionHandler.turn_cw(self.direction)
        self.motor_directions = RIGHT
        self.turn()

    def turn(self):
        start_time = time.time()
        end_time = time.time()
        while (end_time - start_time) < 0.03:
            self.gpio_handler.motor_change(self.motor_directions)
            end_time = time.time()
        self.motor_directions = STOP
        self.gpio_handler.motor_change(self.motor_directions)

    def move_to_node(self):
        print "in moveToNode"
        dist = 0

        start = time.time()
        self.motor_directions = FORWARD
        self.gpio_handler.motor_change(self.motor_directions)
        '''while dist < 10:
            end = time.time()
            spent = floor(end - start)
            dist = self.config.speed * spent'''
        self.motor_directions = STOP
        self.gpio_handler.motor_change(self.motor_directions)

    def startup(self):
        self.gpio_handler.startup()

    def shutdown(self):
        self.gpio_handler.shutdown()
