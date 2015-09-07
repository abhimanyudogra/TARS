from copy import copy
from constants import *
from utility import DirectionHandler


class Heuristic:
    def __init__(self, h, g, f):
        self.h = h
        self.g = g
        self.f = f


class Node:
    def __init__(self, parent, heuristic, num, x, y, sorted_f, path, parent_ancestors, priority_queue):
        self.num = num
        self.parent = parent
        self.heuristic = heuristic
        self.x = x
        self.y = y
        self.left = None
        self.front = None
        self.right = None
        self.ancestors = copy(parent_ancestors)
        if self.parent == -1:
            self.path = []
        else:
            self.path = copy(path)
            if self.heuristic.f not in priority_queue:
                priority_queue[self.heuristic.f] = []
            priority_queue[self.heuristic.f].append(self)
            sorted_f.append(self.heuristic.f)

            self.path.append((parent.x, parent.y))
            self.ancestors.add((parent.x, parent.y))

        sorted_f.sort()


class AStar:
    def __init__(self, config, radar, tars):
        self.config = config
        self.open_list = {}
        self.closed_list = {}
        self.destination = (config.destination_x, config.destination_y)
        self.priority_queue = {}
        self.directions = [NORTH, EAST, SOUTH, WEST]

        self.radar = radar
        self.tars = tars

    def run(self):
        self.tars.startup()
        self.a_star_search()
        self.tars.shutdown()

    def a_star_search(self):
        # initializing
        num = 1
        sorted_f = []
        heuristic = self.calculate_hgf(0, 0, -1)
        curr_node = Node(-1, heuristic, num, 0, 0, sorted_f, [], set(), self.priority_queue)
        curr = (0, 0)
        self.closed_list[tuple(curr)] = curr_node

        while curr != self.destination:
            print "curr node " + str(curr)
            self.update_surrounding(curr_node, num, sorted_f)
            next_node = self.find_next_node(sorted_f)
            if not next_node:
                break

            curr_dir = self.tars.move_to_destination(curr_node, next_node)

            curr_node = next_node
            curr = (curr_node.x, curr_node.y)
            print "next node " + str(curr)

            self.radar.update(BOT, curr)
            self.radar.render()

            self.open_list.pop(tuple(curr))
            self.closed_list[tuple(curr)] = curr_node

        if (curr_node.x, curr_node.y) == self.destination:
            print "shortest path: " + str(curr_node.path)
            self.radar.update(SHORTEST_PATH, curr_node.path)
            self.radar.render()
            print "reached destination"

    def calculate_hgf(self, source_x, source_y, parent_g):
        h_value = abs(self.destination[0] - source_x) + abs(self.destination[1] - source_y)
        g_value = parent_g + 1
        f_value = h_value + g_value
        return Heuristic(h_value, g_value, f_value)

    def update_surrounding(self, curr_node, num, sorted_f):
        child_nodes = []
        scan_sequence = ["turn_left", "turn_right", "turn_right"]

        left_child_direction = DirectionHandler.turn_acw(self.tars.direction)
        middle_child_direction = self.tars.direction
        right_child_direction = DirectionHandler.turn_cw(self.tars.direction)
        child_directions = [left_child_direction, middle_child_direction, right_child_direction]

        for (elem, move) in zip(child_directions, scan_sequence):
            getattr(self.tars, move)()
            child_node = None
            child = (curr_node.x + elem[0], curr_node.y + elem[1])
            '''if next_step not in [(-2, 1), (-2, -1), (-1, -1), (1, -1), (2, -1), (2, 0)
                , (2, 1), (1, 1), (0, 1), (-1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (1, 5), (0, 5), (-1, 5), (-1, 4),
                                 (-1, 3), (0, 3)]:'''
            '''if next_step not in [(-2, 2), (-2, 1), (-2, -0), (-2, -1), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
                                 (2, -1), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (-1, 2)]:'''
            if self.tars.gpio_handler.obstacle_detected() != 1:
                node_existence = self.node_exists(child)
                if node_existence == "none":
                    heuristic = self.calculate_hgf(child[0], child[1], curr_node.heuristic.g)
                    child_node = Node(curr_node, heuristic, num, child[0], child[1], sorted_f,
                                      curr_node.path, curr_node.ancestors, self.priority_queue)
                    self.open_list[child] = child_node
                elif node_existence == "open":
                    child_node = self.open_list[child]
                    heuristic = self.calculate_hgf(child[0], child[1], curr_node.heuristic.g)
                    if heuristic.f < child_node.heuristic.f:
                        sorted_f.remove(child_node.heuristic.f)
                        for item in self.priority_queue[child_node.heuristic.f]:
                            if child == (item.x, item.y):
                                self.priority_queue[child_node.heuristic.f].remove(item)
                                break
                        child_node = Node(curr_node, heuristic, num, child[0], child[1],
                                          sorted_f, curr_node.path, curr_node.ancestors, self.priority_queue)
                        self.open_list[child] = child_node
            else:
                print "obstacle found at: (" + str(child[0]) + "," + str(child[1]) + ")"
                self.radar.update(WALL, child)
                self.radar.render()
            child_nodes.append(child_node)
        curr_node.left, curr_node.front, curr_node.right = child_nodes
        self.tars.turn_left()

    # function to check if node exists
    def node_exists(self, coordinates):
        if self.open_list.keys().__contains__(coordinates):
            return "open"
        elif self.closed_list.keys().__contains__(coordinates):
            return "closed"
        else:
            return "none"

    def find_next_node(self, sorted_f):
        if sorted_f:
            next_min_f = sorted_f[0]
            sorted_f.pop(0)
            if self.priority_queue[next_min_f]:
                next_node = self.priority_queue[next_min_f].pop()
                return next_node
        return None


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
