from copy import copy
import time
from gpio_handler import *


class TARS:
    def __init__(self, config, gpio_handler):
        self.current_direction = (0, 0)
        self.directions = [[0, 1], [-1, 0], [1, 0], [0, -1]]
        self.config = config
        self.gpio_handler = gpio_handler

    def move_to_destination(self, curr_node, curr_dir, next_node):
        if next_node.parent != curr_node:
            print "backtracking..."
            common_ancestor = self.find_common_ancestor(curr_node, next_node)
            path_between = self.create_path(curr_node, next_node, common_ancestor)
            curr_dir = self.traverse_between(path_between, curr_dir)
        else:
            if next_node == curr_node.left:
                curr_dir = self.turn_left(curr_dir)
            if next_node == curr_node.right:
                curr_dir = self.turn_right(curr_dir)
            self.current_direction = (1, 1)
            self.move_to_node()
        return curr_dir

    def find_common_ancestor(self, curr_node, next_node):
        path = copy(curr_node.path)
        path.reverse()
        for node in path:
            if node in next_node.ancestors:
                return node

    def traverse_between(self, path, curr_dir):
        curr_dir = self.turn_right(curr_dir)
        curr_dir = self.turn_right(curr_dir)
        index = 0
        self.current_direction = (1, 1)
        while index != len(path) - 1:
            curr = path[index]
            nxt = path[index + 1]
            if curr_dir == self.directions[0]:
                if nxt[0] < curr[0]:
                    curr_dir = self.turn_left(curr_dir)
                elif nxt[0] > curr[0]:
                    curr_dir = self.turn_right(curr_dir)
            elif curr_dir == self.directions[1]:
                if nxt[1] < curr[1]:
                    curr_dir = self.turn_left(curr_dir)
                elif nxt[1] > curr[1]:
                    curr_dir = self.turn_right(curr_dir)
            elif curr_dir == self.directions[2]:
                if nxt[1] < curr[1]:
                    curr_dir = self.turn_right(curr_dir)
                elif nxt[1] > curr[1]:
                    curr_dir = self.turn_left(curr_dir)
            else:
                if nxt[0] < curr[0]:
                    curr_dir = self.turn_right(curr_dir)
                elif nxt[0] > curr[0]:
                    curr_dir = self.turn_left(curr_dir)
            self.move_to_node()
            index += 1
        return curr_dir

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

    def turn_left(self, curr_dir):
        if curr_dir == self.directions[0]:
            curr_dir = self.directions[1]
        elif curr_dir == self.directions[1]:
            curr_dir = self.directions[3]
        elif curr_dir == self.directions[2]:
            curr_dir = self.directions[0]
        else:
            curr_dir = self.directions[2]
        self.current_direction = (1, 2)
        start_time = time.time()
        end_time = time.time()
        while (end_time - start_time) < 0.03:
            self.gpio_handler.motor_change(self.current_direction)
            end_time = time.time()
        self.current_direction = (0, 0)
        self.gpio_handler.motor_change(self.current_direction)
        return curr_dir

    def turn_right(self, curr_dir):
        if curr_dir == self.directions[0]:
            curr_dir = self.directions[2]
        elif curr_dir == self.directions[1]:
            curr_dir = self.directions[0]
        elif curr_dir == self.directions[2]:
            curr_dir = self.directions[3]
        else:
            curr_dir = self.directions[1]
        self.current_direction = (2, 1)
        start_time = time.time()
        end_time = time.time()
        while (end_time - start_time) < 0.03:
            self.gpio_handler.motor_change(self.current_direction)
            end_time = time.time()
        self.current_direction = (0, 0)
        self.gpio_handler.motor_change(self.current_direction)
        return curr_dir

    def move_to_node(self):
        print "in moveToNode"
        dist = 0
        start = time.time()
        self.current_direction = (1, 1)
        self.gpio_handler.motor_change(self.current_direction)
        '''while dist < 10:
            end = time.time()
            spent = floor(end - start)
            dist = self.config.speed * spent'''
        self.current_direction = (0, 0)
        self.gpio_handler.motor_change(self.current_direction)

    def startup(self):
        self.gpio_handler.startup()

    def shutdown(self):
        self.gpio_handler.shutdown()
