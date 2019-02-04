import socket
from threading import Thread


# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        #(print "New server socket thread started for " + ip + ":" + str(port)
        print ("New server on socket thread for " + str(ip) + ":" + str(port))

    def run(self):
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                print ("Server received data: %s" % data)
                # MESSAGE = raw_input("Multithreaded Python server : Enter Response from Server/Enter exit:")
                # if MESSAGE == 'exit':
                #     print ("exit client")
                #     break

                if data == "data_1":
                    conn.sendall(data)
                    #conn.send(data)  # echo
                    break
        finally:
            # Clean up the connection
            conn.close()


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '192.168.56.104'
TCP_PORT = 2004
BUFFER_SIZE = 16  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpServer.listen(4)
    print ("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join() 