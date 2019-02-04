import socket
import sys
import time


import serial
port = "COM4"
port = "/dev/ttyS0" # en computador face
port = "/dev/ttyUSB0" # en mv ubuntu del mac
baud = 115200
ser = serial.Serial(port, baud, timeout=1)
# open the serial port
if ser.isOpen():
	print(ser.name + ' is open...')
time.sleep(2)

habilitar_puerta = False
def open_door(cmd):
    print ("openning door")
    #port = "/dev/ttyUSB0"

    while True:
        #cmd = "r"
        if cmd == 'exit':
            ser.close()
            exit()
        else:
            #ser.write(cmd.encode('ascii') + '\r\n')
            #data = bytearray(b'r')
            ser.write(b"r")
            #out = ser.read()
		 #out = "r"
            #print('Receiving...' + out)
            break
    print ("Door opened")



def door_server():
    global habilitar_puerta
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    #server_address = ('192.168.222.130', 7000)
    server_address = ('127.0.0.1', 7000)
    print ('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    print (socket.gethostname())

    while True:
        # Wait for a connection
        print ('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print ('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print ('received in server "%s"' % data)
                if data == "open_door" :
                    print ('sending data back to the client')
                    connection.sendall(data)

                    # send "r" to the serial port to open the door
                    cmd = "r"
                    if habilitar_puerta == True:
                        open_door(cmd)
                        print ("waiting 5 seconds")
                        time.sleep(5)
                        print ("waiting done")
                    #time.sleep(0.5)


                elif data == "enable_door":
                    print ('sending data back to the client recepcion')
                    connection.sendall(data)
                    habilitar_puerta = True

                elif data == "disable_door":
                    print ('sending data back to the client recepcion')
                    connection.sendall(data)
                    habilitar_puerta = False

                else:
                    print ('no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()

if __name__ == "__main__":
	door_server()






