from gpio_handler import GPIOHandler
import time
from copy import copy
from math import floor
from constants import *


class Node:
    def __init__(self, parent, h_value, g_value, f_value, num, x, y, dirn, sorted_f, path1, set1, priority_queue):
        self.num = num
        self.parent = parent
        self.h_value = h_value
        self.g_value = g_value
        self.f_value = f_value
        self.x = x
        self.y = y
        self.left = None
        self.front = None
        self.right = None
        self.direction = dirn
        if self.parent == -1:
            self.path = []
            self.ancestors = copy(set1)
        else:
            self.path = copy(path1)
            if f_value not in priority_queue:
                priority_queue[f_value] = []
            priority_queue[f_value].append(self)
            sorted_f.append(f_value)
            self.path.append((parent.x, parent.y))
            self.ancestors = copy(set1)
            self.ancestors.add((parent.x, parent.y))
        sorted_f.sort()


class AStar:
    def __init__(self, config, radar, tars):
        self.config = config
        self.open_list = {}
        self.closed_list = {}
        self.destination = (config.destination_x, config.destination_y)
        self.priority_queue = {}
        self.directions = [[0, 1], [-1, 0], [1, 0], [0, -1]]

        self.radar = radar
        self.tars = tars

    def run(self):
        self.tars.startup()
        self.a_star_search()
        self.tars.shutdown()

    def a_star_search(self):
        # initializing
        curr_dir = self.directions[0]
        num = 1
        sorted_f = []
        (h_value, g_value, f_value) = self.calculate_hgf(0, 0, -1)
        curr_node = Node(-1, h_value, g_value, f_value, num, 0, 0, curr_dir, sorted_f, [], set(), self.priority_queue)
        parent_node = curr_node
        curr = (0, 0)
        self.closed_list[tuple(curr)] = curr_node

        while curr != self.destination:
            print "curr node " + str(curr)
            self.update_surrounding(curr_node, num, curr_dir, sorted_f)
            next_node = self.find_next_node(sorted_f)
            curr_dir = self.tars.move_to_destination(curr_node, curr_dir, next_node)
            curr_node = next_node
            curr = (curr_node.x, curr_node.y)
            print "next node " + str(curr)
            self.radar.update(BOT, curr)
            self.radar.render()
            self.open_list.pop(tuple(curr))
            self.closed_list[tuple(curr)] = curr_node
        print "shortest path: " + str(curr_node.path)
        self.radar.update(SHORTEST_PATH, curr_node.path)
        self.radar.render()
        print "reached destination"

    def calculate_hgf(self, source_x, source_y, parent_g):
        h_value = abs(self.destination[0] - source_x) + abs(self.destination[1] - source_y)
        g_value = parent_g + 1
        f_value = h_value + g_value
        return h_value, g_value, f_value

    def update_surrounding(self, curr_node, num, curr_dir, sorted_f):
        if curr_dir == self.directions[0]:
            curr_list = [self.directions[1], self.directions[0], self.directions[2]]
        elif curr_dir == self.directions[1]:
            curr_list = [self.directions[3], self.directions[1], self.directions[0]]
        elif curr_dir == self.directions[2]:
            curr_list = [self.directions[0], self.directions[2], self.directions[3]]
        else:
            curr_list = [self.directions[2], self.directions[3], self.directions[1]]
        nodes = []
        move_list = ["turn_left", "turn_right", "turn_right"]
        # turn_left(curr_dir)
        for (elem, move) in zip(curr_list, move_list):
            curr_dir = getattr(self.tars, move)(curr_dir)
            # if self.tars.gpio_handler.obstacle_detected() != 1:
            next_step = (curr_node.x + elem[0], curr_node.y + elem[1])
            if next_step not in [(-2, 1), (-2, -1), (-1, -1), (1, -1), (2, -1), (2, 0)
                , (2, 1), (1, 1), (0, 1), (-1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (-1, 5), (-1, 4),
                                 (-1, 3), (0, 3)]:
                if self.check_node_exists(next_step) == "doesn't exist":
                    (h_value, g_value, f_value) = self.calculate_hgf(next_step[0], next_step[1],
                                                                     curr_node.g_value)
                    num += 1
                    node = Node(curr_node, h_value, g_value, f_value, num, next_step[0], next_step[1],
                                curr_dir, sorted_f, curr_node.path, curr_node.ancestors, self.priority_queue)
                    self.open_list[next_step] = node
                elif self.check_node_exists(next_step) == "closed":
                    node = None
                else:
                    node = self.check_node_exists(next_step)
                    (h_value, g_value, f_value) = self.calculate_hgf(next_step[0], next_step[1],
                                                                     curr_node.g_value)
                    if f_value < node.f_value:
                        sorted_f.remove(node.f_value)
                        for item in self.priority_queue[node.f_value]:
                            if next_step == (item.x, item.y):
                                self.priority_queue[node.f_value].remove(item)
                                break
                        node = Node(curr_node, h_value, g_value, f_value, num, next_step[0],
                                    next_step[1], curr_dir,
                                    sorted_f, curr_node.path, curr_node.ancestors, self.priority_queue)
                        self.open_list[next_step] = node
            else:
                node = None
                print "obstacle found at: (" + str(next_step[0]) + "," + str(next_step[1]) + ")"
                self.radar.update(WALL, next_step)
            nodes.append(node)
        left_node, front_node, right_node = nodes
        curr_dir = self.tars.turn_left(curr_dir)
        curr_node.left = left_node
        curr_node.front = front_node
        curr_node.right = right_node

    # function to check if node exists
    def check_node_exists(self, coordinates):
        if self.open_list.keys().__contains__(coordinates):
            return self.open_list[coordinates]
        elif self.closed_list.keys().__contains__(coordinates):
            return "closed"
        else:
            return "doesn't exist"

    def find_next_node(self, sortedF):
        if sortedF:
            next_min_f = sortedF[0]
            sortedF.pop(0)
        else:
            print "no minf"
        if self.priority_queue[next_min_f]:
            next_node = self.priority_queue[next_min_f].pop()
        else:
            print "no node in minF"
            return None
        return next_node


'''#TEST
cfg = {
    "speed": 65,
    "obstacle_distance": 10,
    "window_x": 768,
    "window_y": 768,
    "destination_x" : 2,
    "destination_y" : 4
}
if __name__ == "__main__":
    radar = Radar((cfg["destination_x"],cfg["destination_y"]))
    AStar(main.Config(**cfg)).run()'''
