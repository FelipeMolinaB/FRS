import socket
import sys
import skt_utilities
message = 'open_door'
ip = '127.0.0.1'
skt_utilities.send_data_to_server_skt(message,ip)
