import socket
import sys
import thread


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import variables


def request_open_door(name, other):

    # Creatae a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #server_address = ('192.168.56.104', 7001)
    server_address = (variables.IP_SERVER, variables.PORT_SERVER)
    #server_address = (ip, port)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:

        # Send data
        message = 'open_door/' + name
        print( 'sending "%s"' % message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        data_received = ""
        i = 0
        while amount_received < amount_expected:
            data_received = sock.recv(1024)
            amount_received += len(data_received)
            i += 1
            if  i > 1024:
                print ("server do not respond or response tooo large")
                break
        print ('received "%s"' % data_received)

    finally:
        print ('closing socket')
        sock.close()

def open_door_face(name):
    thread.start_new_thread(request_open_door, (name, 0))