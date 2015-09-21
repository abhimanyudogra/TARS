__author__ = "Niharika Dutta and Abhimanyu Dogra"

import socket
import sys

from server_constants import *


class ServerSocket:
    """
    Manages the server side socket network and sending/receiving of messages through it.
    """

    def __init__(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'SERVER : Socket created'

        try:
            self.soc.bind((HOST, PORT))
        except socket.error, msg:
            print 'SERVER : Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'SERVER : Socket bind complete'
        self.soc.listen(10)
        print 'SERVER : Socket now listening'
        self.conn, addr = self.soc.accept()
        print 'SERVER : Connected with ' + addr[0] + ':' + str(addr[1])

    def listen(self):

        print "SERVER : Waiting for message"
        msg = self.conn.recv(1024)
        print "SERVER : Message received : " + msg
        return msg

    def reply(self, msg):
        print "SERVER : Sending reply : " + msg
        self.conn.sendall(msg)
        print "SERVER : Reply Sent"

    def shutdown(self):
        print "SERVER : Shutting down"
        self.conn.close()
        self.soc.close()
