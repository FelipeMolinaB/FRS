import socket
import sys

# Creatae a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.56.108', 7001)
#server_address = ('127.0.0.1', 7000)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:

    # Send data
    message = 'close_server_socket'
    print( 'sending "%s"' % message)
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    data_received = ""
    while amount_received < amount_expected:
        data_received = sock.recv(1024)
        amount_received += len(data_received)
    print ('received "%s"' % data_received)

finally:
    print ('closing socket')
    sock.close()