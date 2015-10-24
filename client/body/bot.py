__author__ = "Niharika Dutta and Abhimanyu Dogra"

import time

from client.utility.client_constants import *
from client.utility.utilities import DirectionHandler, GraphHandler, ClientCameraHandler


class Bot:
    """
    TARS class handles the behavior of the Raspberry Pi controlled bot hardware. Interacts with the hardware : motors,
    obstacle detector et cetera, by sending messages to the GPIOHandler module on the server via socket network.
    It acts like an interface between the brain (AI) and the hardware (GPIO).
    """

    def __init__(self, config, soc):
        self.motor_directions = STOP
        self.config = config
        self.client_socket = soc
        self.direction = NORTH
        self.radar = None

    def initiate(self):
        self.client_socket.send(STARTUP)

    def close(self):
        self.client_socket.send(SHUTDOWN)

    def move_to_destination(self, curr_node, next_node):
        print "BOT : Moving to destination " + str(curr_node) + " from " + str(next_node)
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
        print "BOT : Traversing path"
        self.turn_right()
        self.turn_right()
        index = 0
        self.motor_directions = FORWARD
        while index != len(path) - 1:
            curr_node = path[index]
            next_node = path[index + 1]
            self.radar.update(BOT, curr_node)
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
        print "BOT : turning left"
        self.direction = DirectionHandler.turn_acw(self.direction)
        self.motor_directions = LEFT
        self.turn()

    def turn_right(self):
        print "BOT : turning right"
        self.direction = DirectionHandler.turn_cw(self.direction)
        self.motor_directions = RIGHT
        self.turn()

    def turn(self):
        start_time = time.time()
        end_time = time.time()
        self.client_socket.send(self.construct_message(self.motor_directions, self.config[MOTOR_TURN_SPEED]))
        while (end_time - start_time) < self.config[BOT_TURN_TIME]:
            end_time = time.time()
        self.motor_directions = STOP
        self.client_socket.send(self.construct_message(self.motor_directions, self.config[MOTOR_TURN_SPEED]))

    def click(self, child, image_index):
        image_name = IMAGES_SEQUENCE[image_index]
        print "BOT : Clicking picture"
        self.client_socket.send(CLICK_PICTURE)
        self.client_socket.receive()
        if self.client_socket.camera_queue:
            reply = self.client_socket.camera_queue.pop(0)
        else:
            print "No image received from camera"
            return None
        print "BOT : Received image"
        return reply

    def move_to_node_ahead(self):
        print "BOT : Moving to node ahead"
        start_time = time.time()
        end_time = time.time()
        self.motor_directions = FORWARD
        self.client_socket.send(self.construct_message(self.motor_directions, self.config[MOTOR_SPEED]))
        while (end_time - start_time) < self.config[BOT_INTER_NODE_TIME]:
            end_time = time.time()
        self.motor_directions = STOP
        self.client_socket.send(self.construct_message(self.motor_directions, self.config[MOTOR_SPEED]))

    def detect_obstacle(self):
        print "BOT : Detecting obstacle"
        self.client_socket.send(DETECT_OBSTACLE)
        self.client_socket.receive()
        if self.client_socket.gpio_queue:
            reply = self.client_socket.gpio_queue.pop(0)
        else:
            print "No reply received for obstacle detection"
        print "BOT : Received reply :" + reply
        return reply == "True"

    def take_a_picture(self, child, image_index):
        image_byte = self.click(child, image_index)
        ClientCameraHandler.convert_bytes_to_image(image_byte, child, image_index)
        return "Image received and stored"

    def construct_message(self, directions, speed):
        return MOTOR_CHANGE + "|" + str(directions) + "|" + str(speed)

    def set_radar(self, radar):
        self.radar = radar
