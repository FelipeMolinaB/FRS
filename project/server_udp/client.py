import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import socket
import variables
import gc
from cStringIO import StringIO
import numpy as np

class CameraClient(object):

    def send_data_to_udp_server(self,message):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (variables.IP_SERVER_UDP, variables.PORT_SERVER_UDP)
        self.socket.connect(self.server_address)
        data = False
        try:
            sent = self.socket.sendall(message)
            data,_ = self.socket.recvfrom(1024)
            self.socket.close()
        except:
            raise
        finally:
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            return bool(data)


class ImageClient(object):

    def send_image(self,image):
        data = False
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_address = (variables.IP_SERVER_IM, variables.PORT_SERVER_IM)
            self.socket.connect(self.server_address)
            image = image.tobytes()
            for i in range(int(np.ceil(len(image)/1024))):
                try:
                    sent = self.socket.sendall(image[(i*1024):((i+1)*1024)])
                except:
                    sent = self.socket.sendall(image[(i*1024):])
                data,_ = self.socket.recvfrom(1024)
            sent = self.socket.sendall(b'\xa5'*1024)
            data = self.socket.recvfrom(1024)
            self.socket.close()
        except:
            raise
        finally:
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            return bool(data)
