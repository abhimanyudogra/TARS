import socket  # for sockets
import sys  # for exit
from TARS.client.utilities.client_constants import *


class ClientSocket:
    def __init__(self):
        # create an INET, STREAMing socket
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'CLIENT : Failed to create socket'
            sys.exit()

        print 'CLIENT : Socket Created'

        # Connect to remote server
        self.soc.connect((TARS_IP, PORT))
        print 'CLIENT : Socket connected to ip : ' + TARS_IP

    def send(self, msg):
        print "CLIENT : Sending message : " + msg
        try:
            # Set the whole string
            self.soc.sendall(msg)
        except socket.error:
            # Send failed
            print 'CLIENT : Message sending failed'
            sys.exit()

        print 'CLIENT : Message sent successfully'

    def receive(self):
        print "CLIENT : Waiting for reply"
        reply = self.soc.recv(4096)
        print "CLIENT : Received reply : " + reply
        return reply

    def close(self):
        print "CLIENT : Closing socket"
        self.soc.close()


if __name__ == "__main__":
    c = ClientSocket()
    for i in xrange(0, 10):
        c.send(str(i))
        print c.receive()
    print "closing client"
    c.close()

