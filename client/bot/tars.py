from TARS.client.utilities.client_constants import *
from TARS.client.utilities.utility import DirectionHandler, GraphHandler
from TARS.client.csocket.client_handler import ClientSocket
import time


class TARS:
    """
    TARS class handles the behavior of the Raspberry Pi controlled bot. Interacts with the hardware : motors, obstacle
    detector et cetera, using the GPIOHandler module. Acts like an interface between the Algorithmic or manual
    movement determining modules and the GPIO module.
    """

    def __init__(self, config, soc):
        self.motor_directions = STOP
        self.config = config
        self.client_socket = soc
        self.direction = NORTH

    def move_to_destination(self, curr_node, next_node):
        print "TARS : Moving to destination : " + str(next_node) + " from " + str(curr_node)
        if next_node.parent != curr_node:
            common_ancestor = GraphHandler.find_common_ancestor(curr_node, next_node)
            path_between = GraphHandler.create_path(curr_node, next_node, common_ancestor)
            self.traverse(path_between)
        else:
            if next_node == curr_node.left:
                self.turn_left()
            if next_node == curr_node.right:
                self.turn_right()
            self.motor_directions = FORWARD
            self.move_to_node_ahead()

    def traverse(self, path):
        print "TARS : Traversing path"
        self.turn_right()
        self.turn_right()
        index = 0
        self.motor_directions = FORWARD
        while index != len(path) - 1:
            curr_node = path[index]
            next_node = path[index + 1]
            if self.direction == NORTH:
                if next_node[0] < curr_node[0]:
                    self.turn_left()
                elif next_node[0] > curr_node[0]:
                    self.turn_right()
            elif self.direction == WEST:
                if next_node[1] < curr_node[1]:
                    self.turn_left()
                elif next_node[1] > curr_node[1]:
                    self.turn_right()
            elif self.direction == EAST:
                if next_node[1] < curr_node[1]:
                    self.turn_right()
                elif next_node[1] > curr_node[1]:
                    self.turn_left()
            else:
                if next_node[0] < curr_node[0]:
                    self.turn_right()
                elif next_node[0] > curr_node[0]:
                    self.turn_left()
            self.move_to_node_ahead()
            index += 1

    def turn_left(self):
        print "TARS : turning left"
        self.direction = DirectionHandler.turn_acw(self.direction)
        self.motor_directions = LEFT
        self.turn()

    def turn_right(self):
        print "TARS : turning right"
        self.direction = DirectionHandler.turn_cw(self.direction)
        self.motor_directions = RIGHT
        self.turn()

    def turn(self):
        start_time = time.time()
        end_time = time.time()
        self.client_socket.send(MOTOR_CHANGE + str(self.motor_directions))
        while (end_time - start_time) < MOTOR_TURN_TIME_90:
            end_time = time.time()
        self.motor_directions = STOP
        self.client_socket.send(MOTOR_CHANGE + str(self.motor_directions))

    def move_to_node_ahead(self):
        print "TARS : Moving to node ahead"
        start_time = time.time()
        end_time = time.time()
        self.motor_directions = FORWARD
        self.client_socket.send(MOTOR_CHANGE + str(self.motor_directions))
        while (end_time - start_time) < MOTOR_MOVE_10_CM_TIME:
            end_time = time.time()
        self.motor_directions = STOP
        self.client_socket.send(MOTOR_CHANGE + str(self.motor_directions))

    def detect_obstacle(self):
        print "TARS : Detecting obstacle"
        self.client_socket.send(DETECT_OBSTACLE)
        reply = self.client_socket.receive()
        print "TARS : Received reply :" + reply
        return reply == "True"
