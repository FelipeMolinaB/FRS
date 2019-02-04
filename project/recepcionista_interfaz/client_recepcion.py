import socket
import sys
import thread


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from server_udp import variables


def set_door_mode(mode):

    # Creatae a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #server_address = ('192.168.56.104', 7001)
    #server_address = ('192.168.56.108', variables.PORT_SERVER_TCP)
    server_address = (variables.IP_SERVER_TCP, variables.PORT_SERVER_TCP)
    #server_address = (variables.IP_SERVER, variables.PORT_SERVER)
    #server_address = (ip, port)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:

        # Send data
        message = mode
        print( 'sending "%s"' % message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        data_received = ""
        while amount_received < amount_expected:
            data_received = sock.recv(16)
            amount_received += len(data_received)
        print ('received "%s"' % data_received)

    finally:
        print ('closing socket')
        sock.close()
        return data_received

