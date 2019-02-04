import socket
import sys
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from thread import start_new_thread
import socket

def send_data_to_server_skt(data, ip):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #server_address = ('192.168.222.25', 10000)
    #server_address = ('192.168.39.234', 7000)
    #server_address = ('192.168.222.130', 7000)
    #server_address = ('127.0.0.1', 7000)
    server_address = (ip, 7000)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)

    try:

        # Send data
        message = data
        print ('sending "%s"' % message)
        #c.sendall(message.encode('utf-8'))
        sock.sendall(message.encode('utf-8'))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        # data = "nada"
        # while amount_received < amount_expected:
        #     data = sock.recv(16)
        #     amount_received += len(data)
        # print ('received in client "%s"' % data)


    finally:
        print ('closing socket')
        sock.close()



def open_door_face(data, ip):
    start_new_thread(send_data_to_server_skt,(data, ip))



message = 'open_door'
ip = '127.0.0.1'
send_data_to_server_skt(message,ip)
