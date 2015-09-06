from gpio_handler import GPIOHandler
import time
from copy import copy
from math import floor


class Node:
    def __init__(self, parent, h_value, g_value, f_value, num, x, y, dirn, sorted_f, path1, set1, priority_queue):
        self.Num = num
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
        if f_value not in priority_queue:
            priority_queue[f_value] = []
        if self.parent == -1:
            self.path = []
            self.ancestors = copy(set1)
        else:
            self.path = copy(path1)
            priority_queue[f_value].append(self)
            sorted_f.append(f_value)
            self.path.append((parent.x, parent.y))
            self.ancestors = copy(set1)
            self.ancestors.add((parent.x, parent.y))
        sorted_f.sort()


class AStar:
    def __init__(self, config):
        self.config = config
        self.open_list = {}
        self.closed_list = {}
        self.destination = (config.destination_x, config.destination_y)
        self.priority_queue = {}
        self.current_direction = (0, 0)
        self.directions = [[0, 1], [-1, 0], [1, 0], [0, -1]]
        self.gpio_handler = GPIOHandler(self.config.speed)

    def run(self):
        self.gpio_handler.startup()
        self.a_star_search()

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
            curr_dir = self.move_tars_to_destination(curr_node, curr_dir, next_node)
            curr_node = next_node
            curr = (curr_node.x, curr_node.y)
            print "next node " + str(curr)
            self.open_list.pop(tuple(curr))
            self.closed_list[tuple(curr)] = curr_node
        print "shortest path: " + str(curr_node.path)
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
        move_list = [self.turn_left, self.turn_right, self.turn_right]
        # turn_left(curr_dir)
        for (elem, move) in zip(curr_list, move_list):
            curr_dir = move(curr_dir)
            if self.gpio_handler.obstacle_detected() != 1:
                if self.check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1])) == "doesn't exist":
                    (h_value, g_value, f_value) = self.calculate_hgf(curr_node.x + elem[0], curr_node.y + elem[1],
                                                                     curr_node.Gvalue)
                    num += 1
                    node = Node(curr_node, h_value, g_value, f_value, num, curr_node.x + elem[0],curr_node.y + elem[1],
                                curr_dir, sorted_f, curr_node.path, curr_node.ancestors, self.priority_queue)
                    self.open_list[(curr_node.x + elem[0], curr_node.y + elem[1])] = node
                elif self.check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1])) == "closed":
                    node = None
                else:
                    node = self.check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1]))
                    (h_value, g_value, f_value) = self.calculate_hgf(curr_node.x + elem[0], curr_node.y + elem[1],
                                                                     curr_node.Gvalue)
                    if f_value < node.Fvalue:
                        sorted_f.remove(node.Fvalue)
                        for item in self.priority_queue[node.Fvalue]:
                            if (curr_node.x + elem[0], curr_node.y + elem[1]) == (item.x, item.y):
                                self.priority_queue[node.Fvalue].remove(item)
                                break
                        node = Node(curr_node, h_value, g_value, f_value, num, curr_node.x + elem[0],
                                    curr_node.y + elem[1], curr_dir,
                                    sorted_f, curr_node.path, curr_node.ancestors, self.priority_queue)
                        self.open_list[(curr_node.x + elem[0], curr_node.y + elem[1])] = node
            else:
                node = None
            nodes.append(node)
        left_node, front_node, right_node = nodes
        curr_dir = self.turn_left(curr_dir)
        curr_node.left = left_node
        curr_node.front = front_node
        curr_node.right = right_node

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
        self.gpio_handler.motor_change()
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
            self.gpio_handler.motor_change()
            end_time = time.time()
        self.current_direction = (0, 0)
        self.gpio_handler.motor_change()
        return curr_dir

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
            return
        return next_node

    def move_tars_to_destination(self, curr_node, curr_dir, next_node):
        if next_node.parent != curr_node:
            print "backtracking..."
            commonAncestor = self.find_common_ancestor(curr_node, next_node)
            path_between = self.create_path(curr_node, next_node, commonAncestor)
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

    def traverse_between(self,path, curr_dir):
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

    def move_to_node(self):
        print "in moveToNode"
        dist = 0
        start = time.time()
        self.current_direction = (1, 1)
        self.gpio_handler.motor_change()
        while dist < 10:
            end = time.time()
            spent = floor(end - start)
            dist = self.speed * spent
        self.current_direction = (0, 0)
        self.motor_change()
        return
