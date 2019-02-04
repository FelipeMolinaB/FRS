#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import thread

def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(16)
        #do some checks and if msg == someWeirdSignal: break:
        print (addr, ' >> ', msg)
        #msg = raw_input('SERVER >> ')
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.sendall(msg)
    clientsocket.close()

#s = socket.socket()         # Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # Get local machine name
port = 7000                # Reserve a port for your service.

print ('Server started!')
print ('Waiting for clients...')

#s.bind((host, port))        # Bind to the port

server_address = ('127.0.0.1', 7000)
print ('starting up on %s port %s' % server_address)
s.bind(server_address)
           # Now wait for client connection.

#print 'Got connection from', addr
while True:
    s.listen(1)
    c, addr = s.accept()     # Establish connection with client.
    thread.start_new_thread(on_new_client,(c,addr))
    #Note it's (addr,) not (addr) because second parameter is a tuple
    #Edit: (c,addr)
    #that's how you pass arguments to functions when creating new threads using thread module.
s.close()
