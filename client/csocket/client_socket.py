__author__ = "Niharika Dutta and Abhimanyu Dogra"

import socket
import sys

from TARS.client.utility.client_constants import STANDBY


class ClientSocket:
    """
    Manages the client side socket network and sending/receiving of messages through it.
    """

    def __init__(self, config):
        self.counter = 0
        self.config = config
        # create an INET, STREAMing socket

    def connect(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'CLIENT : Failed to create socket'
            sys.exit()
        print 'CLIENT : Socket Created'
        # Connect to remote server
        self.soc.connect((self.config.raspberry_pi_address, self.config.raspberry_pi_port))
        print 'CLIENT : Socket connected to ip : ' + self.config.raspberry_pi_address

    def send(self, msg):
        try:
            print "CLIENT : Sending message : " + msg
            # Set the whole string
            self.soc.sendall(msg)
            self.counter += 1
            print "CLIENT : Message sent successfully" + " #" + str(self.counter)
        except socket.error:
            # Send failed
            print 'CLIENT : Socket error while sending'
            sys.exit()

    def receive(self):
        try:
            print "CLIENT : Waiting for reply"
            reply = self.soc.recv(4096)
            print "CLIENT : Received reply : " + reply
            return reply
        except socket.error:
            # Send failed
            print 'CLIENT : Socket error while receiving'
            sys.exit()

    def close(self):
        print "CLIENT : Putting server on standby"
        self.send(STANDBY)
        print "CLIENT : Closing socket"
        self.soc.close()
