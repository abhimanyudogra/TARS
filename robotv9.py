try:
    import RPi.GPIO as GPIO

except RuntimeError:
    print("Error importing RPi.GPIO! This must be run as root using sudo")

import sys, tty, termios
import picamera
import time
import os
from getch import getch
import pygame

# photo id
photo_id = 0

# Motor PINs
MOTOR1A = 17    #left fwd
MOTOR1B = 18    #left rev
MOTOR2A = 23    #right fwd
MOTOR2B = 22    #right rev

# freq of pwm outputs
PWM_FREQ = 50 #50hz

# uses processor pin numbering
GPIO.setmode(GPIO.BCM)

# speed = pwm duty cycle, 0 = off, 100 = max
speed = 75
speed2 = 37
# To change speed add or remove 10 - check for <0 and >100

# Camera settings
CAMERA_X = 1296
CAMERA_Y = 972
# Is camera upright / upside down
# Upside down = 180
CAMERA_ROTATE = 180



# server ip address - set to 127.0.0.1 for local connections only, or change to actual address if require access direct from other computers (eg. smartphone) '' = all interfaces
HOST = ''
# unique port number - this happens to be the ip address used in the example setup without the dots
#PORT = 10551
# Using standard port as no other webserver running
PORT = 80
# length of a message - all network messages must be padded to this length 
#MSG_LEN = 20


# global for direction of motors (m1, m2)
#current_direction = (0, 0)



# Change the motor outputs based on the current_direction and speed global variables
def motor_change():
    #print "Update motors to " + str(current_direction[0]) + " " + str(current_direction[1])
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
 

# Takes a picture and stores it in a folder named "photos" 
def take_photo():   
    with picamera.PiCamera() as camera:
        camera.resolution = (CAMERA_X, CAMERA_Y)
        camera.rotation = CAMERA_ROTATE
        dir = os.getcwd()
        photos_folder = os.path.join(dir , "photos")
        if not os.path.exists(photos_folder):
            os.mkdir(photos_folder)		
        camera.capture(os.path.join(photos_folder, "photo" + photo_id + ".jpg"))
        photo_id = photo_id + 1
        camera.close()
        return "OK"




# direction based on number keypad 
# 8 = fwd, 2 = rev, 4 = left, 5 = right, 7 = fwd left, 9 = fwd right, 1 = rev left, 3 = rev right
### These are from the command line version - they are not used in this version. This list will be removed in future edits
direction = {
    # number keys
    '1' : (2, 0),
    '2' : (2, 2),
    '3' : (0, 2),
    '4' : (1, 2),
    '5' : (0, 0),
    '6' : (2, 1),
    '7' : (1, 0),
    '8' : (1, 1),
    '9' : (0, 1)
}




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

exit_flag = False
pygame.init()
pygame.key.set_repeat(100, 100)
window = pygame.display.set_mode((800,480))


while not exit_flag:
    pressed = pygame.key.get_pressed()
    pressed_map = (pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_LEFT)
    if (pressed_map == (1,0,0,0)):
        if current_direction != (1,1):
            current_direction = (1,1)
            motor_change()
            elif event.key == pygame.K_RIGHT:
                if current_direction != (0,1):
                    current_direction = (0,1)
                    motor_change()
            elif event.key == pygame.K_DOWN:
                if current_direction != (2,2):
                    current_direction = (2,2)
                    motor_change()
            elif event.key == pygame.K_LEFT:
                if current_direction != (1,0):
                    current_direction = (1,0)
                    motor_change()
            if event.key == pygame.K_SPACE:
                errStatus = take_photo()
            if event.key == pygame.K_ESCAPE:
                exit_flag = True
        if event.type == pygame.KEYUP:
            if current_direction != (0,0):
                current_direction = (0,0)
                motor_change()

pygame.quit()


'''while exit_flag:
    key = ord(getch())
    if key == 27: # Special key
        key = ord(getch())
        if key == 91:
            key = ord(getch())
            if key == 65: # forward
                current_direction = (1,1)
                motor_change()
            elif key == 67: # right turn
                current_direction = (0,1)
                motor_change()
            elif key == 66: #backward
                current_direction = (2,2)
                motor_change()
            elif key == 68: #left turn
                current_direction = (1, 0)
                motor_change()
    elif key == 97: # A -> fast left turn
        current_direction = (1,2)
        motor_change()
    elif key == 122: #Z -> backward left turn
        current_direction = (0,2)
        motor_change()
    elif key == 115: #S -> fast right turn
        current_direction = (2,1)
        motor_change()
    elif key == 120: #X -> backward right turn
        current_direction = (2,0)
        motor_change()
    elif key == 32: #space -> brake
        current_direction = (0,0)
        motor_change()
    elif key == 112: #P -> take picture
        errStatus = take_photo()'''

                
        
"""next_move = 'g'
while (next_move != 'n'):
    next_move = raw_input()
    if (next_move == 's'):
        current_direction = (0,2)
        motor_change()        
    elif (next_move == 'd'):
        current_direction = (1,2)
        motor_change()
    elif (next_move == 'f'):
        current_direction = (1,0)
        motor_change()
    elif(next_move == 'h'):
        current_direction = (2,0)
        motor_change()
    elif(next_move == 'j'):
        current_direction = (2,1)
        motor_change()
    elif(next_move == 'k'):
        current_direction = (0,1)
        motor_change()
    elif(next_move == 't'):
        current_direction = (1,1)
        motor_change()
    elif(next_move == 'b'):
        current_direction = (2,2)
        motor_change()
    elif(next_move == 'g'):
        current_direction = (0,0)
        motor_change()"""




    
    
# Stop PWM and cleanup - only called if exit from bottle server        
pin1A.stop()
pin1B.stop()
pin2A.stop()
pin1B.stop()
GPIO.cleanup()
