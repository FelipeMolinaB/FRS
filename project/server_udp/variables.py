import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

OPEN_DOOR_FACE = False
#IP_SERVER_TCP = "127.0.0.1"
IP_SERVER_TCP = "192.168.222.130"
IP_SERVER_UDP = "localhost"
PORT_SERVER_TCP = 7002
PORT_SERVER_UDP = 7003

IP_SERVER_IM = "localhost"
PORT_SERVER_IM = 7004
PORT_SERVER_INF = 7005


habilitar_puerta = False
open_door_flag = False
door_bussy = False
name = ""

n_verificacion = 3
min_area = 28000
