import socket
import sys
import thread

# Create a TCP/IP socket


# Bind the socket to the port
server_address = ('192.168.56.104', 7000)
print ('starting up on %s port %s' % server_address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)


def on_new_client(connection,client_address):
    try:
        print ('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print ('received "%s"' % data)
            #if data == "close_server_socket":
            if data:
                print ('sending data back to the client')
                connection.sendall(data)
            else:
                print ('no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()


# Listen for incoming connections
while True:
    try:
        sock.listen(1)
        print ('waiting for a connection')
        connection, client_address = sock.accept()
        thread.start_new_thread(on_new_client, (connection, client_address))
    except:
        sock.close()
        print ("there was an exception")
        break
