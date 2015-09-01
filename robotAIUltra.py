try:
    import RPi.GPIO as GPIO

except RuntimeError:
    print("Error importing RPi.GPIO! This must be run as root using sudo")

import os
import sys
import tty
import termios
import time
import math
import heapq
from copy import copy

# Motor PINs
MOTOR1A = 17    #left fwd
MOTOR1B = 18    #left rev
MOTOR2A = 23    #right fwd
MOTOR2B = 22    #right rev

# freq of pwm outputs
PWM_FREQ = 50 #50hz

# uses processor pin numbering
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 14

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO,GPIO.IN)


# speed = pwm duty cycle, 0 = off, 100 = max
speed = 65
# To change speed add or remove 10 - check for <0 and >100

openList = {}
closedList = {}
destination = (0, 4)
priorityQueue = {}
current_direction = (0, 0)



class Node:
    def __init__(self, parent, H, G, F, num, x, y, dirn, sortedF, path1, set1):
        self.Num = num
        self.parent = parent
        self.Hvalue = H
        self.Gvalue = G
        self.Fvalue = F
        self.x = x
        self.y = y
        self.left = None
        self.front = None
        self.right = None
        self.direction = dirn
        if priorityQueue.has_key(F) == False:
            priorityQueue[F] = []
        if self.parent == -1:
            self.path = []
            self.ancestors = copy(set1)
        else:
            self.path = copy(path1)
            priorityQueue[F].append(self)
            sortedF.append(F)
            self.path.append((parent.x, parent.y))
            self.ancestors = copy(set1)
            self.ancestors.add((parent.x, parent.y))
        sortedF.sort()




def obstacle_detected(x, y):
    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()
    distance = (stop-start) * 17000
    if distance < 10:
        print "obstacle detected"
        return 1
    else:
        return 0


# front,left,right,back
directions = [[0, 1], [-1, 0], [1, 0], [0, -1]]


# Change the motor outputs based on the current_direction and speed global variables
def motor_change():
    print "Update motors to " + str(current_direction[0]) + " " + str(current_direction[1])
    # motor 1
    if (current_direction[0] == 1) :
        pin1A.ChangeDutyCycle(speed)
        pin1B.ChangeDutyCycle(0)
    elif (current_direction[0] == 2) :
        pin1A.ChangeDutyCycle(0)
        pin1B.ChangeDutyCycle(speed)
    # if 0 (stop) or invalid stop anyway
    else :
        pin1A.ChangeDutyCycle(0)
        pin1B.ChangeDutyCycle(0)
    # motor 2
    if (current_direction[1] == 1) :
        pin2A.ChangeDutyCycle(speed)
        pin2B.ChangeDutyCycle(0)
    elif (current_direction[1] == 2) :
        pin2A.ChangeDutyCycle(0)
        pin2B.ChangeDutyCycle(speed)
    # if 0 (stop) or invalid stop anyway
    else :
        pin2A.ChangeDutyCycle(0)
        pin2B.ChangeDutyCycle(0)


# function to check if node exists
def check_node_exists(coordinates):
    if openList.keys().__contains__(coordinates):
        return openList[coordinates]
    elif closedList.keys().__contains__(coordinates):
        return "closed"
    else:
        return "doesn't exist"


def Calculate_HGF(sourceX, sourceY, parentG):
    H = abs(destination[0] - sourceX) + abs(destination[1] - sourceY)
    G = parentG + 1
    F = H + G
    return (H, G, F)


def turn_left(curr_dir):
    if curr_dir == directions[0]:
        curr_dir = directions[1]
    elif curr_dir == directions[1]:
        curr_dir = directions[3]
    elif curr_dir == directions[2]:
        curr_dir = directions[0]
    else:
        curr_dir = directions[2]
    current_direction = (1,2)
    start_time = time.time()
    end_time = time.time()
    while (end_time - start_time) < 0.03:
        motor_change()
        end_time = time.time()
    current_direction = (0,0)
    motor_change()
    return curr_dir


def turn_right(curr_dir):
    if curr_dir == directions[0]:
        curr_dir = directions[2]
    elif curr_dir == directions[1]:
        curr_dir = directions[0]
    elif curr_dir == directions[2]:
        curr_dir = directions[3]
    else:
        curr_dir = directions[1]
    current_direction = (2,1)
    start_time = time.time()
    end_time = time.time()
    while (end_time - start_time) < 0.03:
        motor_change()
        end_time = time.time()
    current_direction = (0,0)
    motor_change()
    return curr_dir


def findCommonAncestor(curr_node, next_node):
    path = copy(curr_node.path)
    path.reverse()
    for node in path:
        if node in next_node.ancestors:
            return node


def traverse_between(path, curr_dir):
    curr_dir = turn_right(curr_dir)
    curr_dir = turn_right(curr_dir)
    index = 0
    current_direction = (1,1)
    while index != len(path) - 1:
        curr = path[index]
        nxt = path[index + 1]
        if curr_dir == directions[0]:
            if nxt[0] < curr[0]:
                curr_dir = turn_left(curr_dir)
                moveToNode()
            elif nxt[0] > curr[0]:
                curr_dir = turn_right(curr_dir)
                moveToNode()
            else:
                moveToNode()
        elif curr_dir == directions[1]:
            if nxt[1] < curr[1]:
                curr_dir = turn_left(curr_dir)
                moveToNode()
            elif nxt[1] > curr[1]:
                curr_dir = turn_right(curr_dir)
                moveToNode()
            else:
                moveToNode()
        elif curr_dir == directions[2]:
            if nxt[1] < curr[1]:
                curr_dir = turn_right(curr_dir)
                moveToNode()
            elif nxt[1] > curr[1]:
                curr_dir = turn_left(curr_dir)
                moveToNode()
            else:
                moveToNode()
        else:
            if nxt[0] < curr[0]:
                curr_dir = turn_right(curr_dir)
                moveToNode()
            elif nxt[0] > curr[0]:
                curr_dir = turn_left(curr_dir)
                moveToNode()
            else:
                moveToNode()
        index += 1
    return curr_dir


def create_path(curr_node, next_node, common_ancestor):
    common_ancestor_idx = curr_node.path.index(common_ancestor)
    subset = slice(common_ancestor_idx,len(curr_node.path))
    path1 = curr_node.path[subset]
    common_ancestor_idx = next_node.path.index(common_ancestor)
    subset = slice(common_ancestor_idx+1,len(next_node.path))
    path2 = next_node.path[subset]
    path2.append((next_node.x, next_node.y))
    path1.reverse()
    path1.extend(path2)
    path1.insert(0, (curr_node.x, curr_node.y))
    return path1


def moveToNode():
    print "in moveToNode"
    dist = 0
    start = time.time()
    current_direction = (1,1)
    motor_change()
    while dist < 10:
        end = time.time()
        spent = math.floor(end - start)
        dist = speed * spent
    current_direction = (0, 0)
    motor_change()
    return


def update_surrounding(curr_node, num, curr_dir, sortedF):
    if curr_dir == directions[0]:
        curr_list = [directions[1], directions[0], directions[2]]
    elif curr_dir == directions[1]:
        curr_list = [directions[3], directions[1], directions[0]]
    elif curr_dir == directions[2]:
        curr_list = [directions[0], directions[2], directions[3]]
    else:
        curr_list = [directions[2], directions[3], directions[1]]
    nodes = []
    move_list = [turn_left, turn_right, turn_right]
    # turn_left(curr_dir)
    for (elem, move) in zip(curr_list, move_list):
        curr_dir = move(curr_dir)
        if obstacle_detected(curr_node.x + elem[0], curr_node.y + elem[1]) != 1:
            if check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1])) == "doesn't exist":
                (H, G, F) = Calculate_HGF(curr_node.x + elem[0], curr_node.y + elem[1], curr_node.Gvalue)
                num += 1
                node = Node(curr_node, H, G, F, num, curr_node.x + elem[0], curr_node.y + elem[1], curr_dir, sortedF,
                            curr_node.path, curr_node.ancestors)
                openList[(curr_node.x + elem[0], curr_node.y + elem[1])] = node
            elif check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1])) == "closed":
                node = None
            else:
                node = check_node_exists((curr_node.x + elem[0], curr_node.y + elem[1]))
                (H, G, F) = Calculate_HGF(curr_node.x + elem[0], curr_node.y + elem[1], curr_node.Gvalue)
                if F < node.Fvalue:
                    sortedF.remove(node.Fvalue)
                    for item in priorityQueue[node.Fvalue]:
                        if (curr_node.x + elem[0], curr_node.y + elem[1]) == (item.x,item.y):
                            priorityQueue[node.Fvalue].remove(item)
                            break
                    node = Node(curr_node, H, G, F, num, curr_node.x + elem[0], curr_node.y + elem[1], curr_dir,
                                sortedF,curr_node.path, curr_node.ancestors)
                    openList[(curr_node.x + elem[0], curr_node.y + elem[1])] = node
        else:
            node = None
        nodes.append(node)
    left_node, front_node, right_node = nodes
    curr_dir = turn_left(curr_dir)
    curr_node.left = left_node
    curr_node.front = front_node
    curr_node.right = right_node


def find_next_node(sortedF):
    if sortedF:
        nextMinF = sortedF[0]
        sortedF.pop(0)
    else:
        print "no minf"
    if priorityQueue[nextMinF]:
        nextNode = priorityQueue[nextMinF].pop()
    else:
        print "no node in minF"
        return
    return nextNode


def move_tars_to_destination(curr_node, curr_dir, next_node):
    if next_node.parent != curr_node:
        print "backtracking..."
        commonAncestor = findCommonAncestor(curr_node, next_node)
        path_between = create_path(curr_node, next_node, commonAncestor)
        curr_dir = traverse_between(path_between, curr_dir)
    else:
        if next_node == curr_node.left:
            curr_dir = turn_left(curr_dir)
        if next_node == curr_node.right:
            curr_dir = turn_right(curr_dir)
        current_direction = (1,1)
        moveToNode()
    return curr_dir


def a_star_search():
    # initializing
    curr_dir = directions[0]
    num = 1
    sortedF = []
    (H, G, F) = Calculate_HGF(0, 0, -1)
    curr_node = Node(-1, H, G, F, num, 0, 0, curr_dir, sortedF, [], set())
    parent_node = curr_node
    curr = (0, 0)
    closedList[tuple(curr)] = curr_node

    while curr != destination:
        print "curr node " + str(curr)
        update_surrounding(curr_node, num, curr_dir, sortedF)
        next_node = find_next_node(sortedF)
        curr_dir = move_tars_to_destination(curr_node, curr_dir, next_node)
        curr_node = next_node
        curr = (curr_node.x, curr_node.y)
        print "next node " + str(curr)
        openList.pop(tuple(curr))
        closedList[tuple(curr)] = curr_node
    print "shortest path: " + str(curr_node.path)
    print "reached destination"
    return



# setup pins
GPIO.setup(MOTOR1A, GPIO.OUT)
GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR2A, GPIO.OUT)
GPIO.setup(MOTOR2B, GPIO.OUT)
#GPIO.setup(PWM_ALL, GPIO.OUT)

pin1A = GPIO.PWM(MOTOR1A, PWM_FREQ)
pin1B = GPIO.PWM(MOTOR1B, PWM_FREQ)
pin2A = GPIO.PWM(MOTOR2A, PWM_FREQ)
pin2B = GPIO.PWM(MOTOR2B, PWM_FREQ)

pin1A.start (0)
pin1B.start (0)
pin2A.start (0)
pin2B.start (0)

a_star_search()


pin1A.stop()
pin1B.stop()
pin2A.stop()
pin1B.stop()
GPIO.cleanup()

