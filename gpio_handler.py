""" UNIT_TEST try:
    import RPi.GPIO as GPIO

except RuntimeError:
    print("Error importing RPi.GPIO! This must be run as root using sudo")     remove after testing"""

import time
from random import randint


class GPIOHandler:
    def __init__(self, speed):
        self.MOTOR1A = 17  # left fwd
        self.MOTOR1B = 18  # left rev
        self.MOTOR2A = 23  # right fwd
        self.MOTOR2B = 22  # right rev

        # freq of pwm outputs
        self.PWM_FREQ = 50  # 50hz

        # uses processor pin numbering
        # UNIT_TEST GPIO.setmode(GPIO.BCM)

        self.TRIG = 15
        self.ECHO = 14

        # UNIT_TEST GPIO.setup(self.TRIG, GPIO.OUT)
        # UNIT_TEST GPIO.output(self.TRIG, 0)

        # UNIT_TEST GPIO.setup(self.ECHO, GPIO.IN)
        self.speed = speed

        # setup pins
        """ UNIT_TEST GPIO.setup(self.MOTOR1A, GPIO.OUT)
        GPIO.setup(self.MOTOR1B, GPIO.OUT)
        GPIO.setup(self.MOTOR2A, GPIO.OUT)
        GPIO.setup(self.MOTOR2B, GPIO.OUT)
        GPIO.setup(PWM_ALL, GPIO.OUT)

        self.pin1A = GPIO.PWM(self.MOTOR1A, self.PWM_FREQ)
        self.pin1B = GPIO.PWM(self.MOTOR1B, self.PWM_FREQ)
        self.pin2A = GPIO.PWM(self.MOTOR2A, self.PWM_FREQ)
        self.pin2B = GPIO.PWM(self.MOTOR2B, self.PWM_FREQ)"""

    def startup(self):
        """ UNIT_TEST self.pin1A.start(0)
        self.pin1B.start(0)
        self.pin2A.start(0)
        self.pin2B.start(0)"""

    def shutdown(self):
        """ UNIT_TEST self.pin1A.stop()
        self.pin1B.stop()
        self.pin2A.stop()
        self.pin1B.stop()
        GPIO.cleanup()"""

    def obstacle_detected(self):
        i = randint(0, 2)
        if i == 0:
            return 1
        return 0
        """ UNIT_TEST GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, 0)

        while GPIO.input(self.ECHO) == 0:
            pass
        start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pass
        stop = time.time()
        distance = (stop - start) * 17000
        if distance < 10:
            print "obstacle detected"
            return 1
        else:
            return 0"""

        # Change the motor outputs based on the current_direction and speed global variables

    def motor_change(self, motor_directions):
        # motor 1
        """ UNIT_TEST if motor_directions[0] == 1:
            self.pin1A.ChangeDutyCycle(self.speed)
            self.pin1B.ChangeDutyCycle(0)
        elif motor_directions[0] == 2:
            self.pin1A.ChangeDutyCycle(0)
            self.pin1B.ChangeDutyCycle(self.speed)
        # if 0 (stop) or invalid stop anyway
        else:
            self.pin1A.ChangeDutyCycle(0)
            self.pin1B.ChangeDutyCycle(0)
        # motor 2
        if motor_directions[1] == 1:
            self.pin2A.ChangeDutyCycle(self.speed)
            self.pin2B.ChangeDutyCycle(0)
        elif motor_directions[1] == 2:
            self.pin2A.ChangeDutyCycle(0)
            self.pin2B.ChangeDutyCycle(self.speed)
        # if 0 (stop) or invalid stop anyway
        else:
            self.pin2A.ChangeDutyCycle(0)
            self.pin2B.ChangeDutyCycle(0)"""
