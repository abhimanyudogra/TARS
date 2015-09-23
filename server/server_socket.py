__author__ = "Niharika Dutta and Abhimanyu Dogra"

import socket
import sys

from server_constants import *


class ServerSocket:
    """
    Manages the server side socket network and sending/receiving of messages through it.
    """

    def __init__(self):
        self.counter = 0
        self.conn, self.addr = None, None
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_queue = []
        print 'SERVER : Socket created'
        try:
            self.soc.bind((HOST, PORT))
        except socket.error, msg:
            print 'SERVER : Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'SERVER : Socket bind complete'
        self.soc.listen(10)
        print 'SERVER : Socket now listening'

    def listen(self):
        if not self.command_queue:
            if not self.conn:
                self.conn, self.addr = self.soc.accept()
                print 'SERVER : Connected with ' + self.addr[0] + ':' + str(self.addr[1])
            try:
                print "SERVER : Waiting for message"
                msg = self.conn.recv(4096)
                commands = [command for command in msg.split(DELIMITER) if command != ""]
                self.counter += len(commands)
                print "SERVER : Message received : " + msg + " #" + str(self.counter)
                self.command_queue.extend(commands)
            except socket.error as e:
                # Send failed
                print 'SERVER : Socket error while receiving' + e.message
                return SOCKET_ERROR
        return self.command_queue.pop(0)

    def reply(self, msg):
        try:
            print "SERVER : Sending reply : " + msg
            self.conn.sendall(msg)
            print "SERVER : Reply Sent"
        except socket.error as e:
            # Send failed
            print 'SERVER : Socket error while sending : ' + e.message
            sys.exit()

    def standby(self):
        print "SERVER : Standing by..."
        self.conn, self.addr = None, None

    def shutdown(self):
        print "SERVER : Shutting down"
        self.conn.close()
        self.soc.close()
