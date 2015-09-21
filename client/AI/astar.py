from TARS.client.utilities.client_constants import *
from TARS.client.utilities.utility import DirectionHandler, Node


class Heuristic:
    """
    Heuristic class handles data about the heuristics for the AStar algorithm.
    """

    def __init__(self, source, destination, parent_g):
        self.h = abs(destination[0] - source[0]) + abs(destination[1] - source[1])
        self.g = parent_g + 1
        self.f = self.h + self.g


class AStar:
    """
    Primary class that controls the AStar algorithm.
    """

    def __init__(self, config, radar, tars):
        self.config = config
        self.open_list = {}
        self.closed_list = {}
        self.destination = (config.destination_x, config.destination_y)
        self.priority_queue = {}
        self.sorted_f = []
        self.directions = [NORTH, EAST, SOUTH, WEST]

        self.radar = radar
        self.tars = tars

    def run(self):
        self.a_star_search()

    def a_star_search(self):
        # initializing
        heuristic = Heuristic((0, 0), self.destination, -1)
        curr_node = Node(-1, heuristic, (0, 0))
        curr = (0, 0)
        self.closed_list[tuple(curr)] = curr_node
        self.radar.render()

        while curr != self.destination:
            if self.check_unreachability():
                break
            self.process_child_nodes(curr_node)
            next_node = self.get_next_node()
            if not next_node:
                break
            self.tars.move_to_destination(curr_node, next_node)
            curr_node = next_node
            curr = (curr_node.x, curr_node.y)
            self.radar.update(BOT, curr)
            self.open_list.pop(tuple(curr))
            self.closed_list[tuple(curr)] = curr_node

        if (curr_node.x, curr_node.y) == self.destination:
            self.radar.update(SHORTEST_PATH, curr_node.path)

    def check_unreachability(self):
        left = (self.destination[0] - 1, self.destination[1])
        right = (self.destination[0] + 1, self.destination[1])
        up = (self.destination[0], self.destination[1] + 1)
        down = (self.destination[0], self.destination[1] - 1)

        if left in self.closed_list and right in self.closed_list and up in self.closed_list and down in self.closed_list:
            return True
        return False

    def create_node(self, parent, heuristic, location, path, parent_ancestors):
        node = Node(parent, heuristic, location, path, parent_ancestors)
        if node.heuristic.f not in self.priority_queue:
            self.priority_queue[node.heuristic.f] = []
        self.priority_queue[node.heuristic.f].append(node)
        self.sorted_f.append(node.heuristic.f)
        self.open_list[location] = node
        return node

    def process_child_nodes(self, curr_node):
        child_nodes = []
        scan_sequence = ["turn_left", "turn_right", "turn_right"]

        left_child_direction = DirectionHandler.turn_acw(self.tars.direction)
        middle_child_direction = self.tars.direction
        right_child_direction = DirectionHandler.turn_cw(self.tars.direction)
        child_directions = [left_child_direction, middle_child_direction, right_child_direction]

        for (child_direction, move) in zip(child_directions, scan_sequence):
            getattr(self.tars, move)()
            child_node = None
            child = (curr_node.x + child_direction[0], curr_node.y + child_direction[1])
            self.radar.update(HIGHLIGHT, child)

            if child not in self.closed_list.keys():
                obstacle_detected = self.tars.detect_obstacle()
                if not obstacle_detected:
                    # if child != (4, 4):
                    heuristic = Heuristic(child, self.destination, curr_node.heuristic.g)
                    if child in self.open_list.keys():
                        old_child_node = self.open_list[child]
                        if heuristic.f < old_child_node.heuristic.f:
                            self.sorted_f.remove(old_child_node.heuristic.f)
                            for node in self.priority_queue[old_child_node.heuristic.f]:
                                if child == (node.x, node.y):
                                    self.priority_queue[old_child_node.heuristic.f].remove(node)
                                    break
                            child_node = self.create_node(curr_node, heuristic, child, curr_node.path,
                                                          curr_node.ancestors)
                    else:
                        child_node = self.create_node(curr_node, heuristic, child, curr_node.path,
                                                      curr_node.ancestors)
                else:
                    self.radar.update(WALL, child)

            child_nodes.append(child_node)
            self.radar.highlights.reset()
        curr_node.left, curr_node.front, curr_node.right = child_nodes
        self.tars.turn_left()

    def get_next_node(self):
        self.sorted_f.sort()
        if self.sorted_f:
            next_min_f = self.sorted_f[0]
            self.sorted_f.pop(0)
            if self.priority_queue[next_min_f]:
                return self.priority_queue[next_min_f].pop()
        return None
