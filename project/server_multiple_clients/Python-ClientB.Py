# Python TCP Client B
import socket 

# host = socket.gethostname()
# port = 2004


host = '192.168.56.104'
#host = '127.0.0.1'
port = 2004


BUFFER_SIZE = 1024
#MESSAGE = raw_input("tcpClientB: Enter message/ Enter exit:")
message = "data_1"
 
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))

# while MESSAGE != 'exit':
#     tcpClientB.send(MESSAGE)
#     data = tcpClientB.recv(BUFFER_SIZE)
#     print " Client received data:", data
#     MESSAGE = raw_input("tcpClientB: Enter message to continue/ Enter exit:")

tcpClientB.sendall(message.encode('utf-8'))


#data = tcpClientB.recv(BUFFER_SIZE)

amount_received = 0
amount_expected = len(message)
data_received = ""
while amount_received < amount_expected:
    data_received = tcpClientB.recv(16)
    amount_received += len(data_received)
    print ('received in client recepcion "%s"' % data_received)


#print (" Client received data:", data)
#MESSAGE = raw_input("tcpClientB: Enter message to continue/ Enter exit:")

tcpClientB.close() 