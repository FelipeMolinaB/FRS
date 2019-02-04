import sys
import os
import thread


sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from server_udp import client

raw_input("Press enter to exit")

message = "open_door/Juancho"
#client.send_data_to_udp_server(message)
thread.start_new_thread(client.send_data_to_udp_server, (message,))

raw_input("Press enter to exit")