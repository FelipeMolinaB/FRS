import socket

IP_SERVER = "localhost"
PORT_SERVER_IM = 7004
PORT_SERVER_INF = 7005

while(True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP_SERVER, PORT_SERVER_INF)
    sock.connect(server_address)
    data = False
    msg = input(">")
    sent = sock.sendall(msg.encode())
    data = sock.recvfrom(1024)
    print(data)
    sock.close()
