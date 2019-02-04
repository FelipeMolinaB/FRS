import socket
import sys
import thread
import time
import serial
import variables
import datetime as dt
from gtts import gTTS
import os
from threading import Thread
from multiprocessing import Process
from sklearn.externals import joblib
#from reporte_de_entrada import variable_reporte_enrtada
import gc
import sys
import time
from server_udp import variables

sys.exc_clear()
sys.exc_traceback = sys.last_traceback = None


class server_habilitar_puerta():

    def __init__(self, server_address = ('192.168.56.108', variables.PORT_SERVER_TCP)):
        self.server_address = server_address
        #server_address = (variables.IP_SERVER, variables.PORT_SERVER)
        print ('starting up on %s port %s' % server_address)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(server_address)
        #self.habilitar_puerta = False

    def open_door_service(self):
        print ("openning door service start")
        while True:
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            print ("variables.habilitar_puerta %s" %variables.habilitar_puerta)


    def on_new_client(self, connection, client_address):
        global open_door_flag, habilitar_puerta, name
        try:
            print ('connection from', client_address)

            # Receive the data in small chunks and retransmit it

            data = connection.recv(16)
            print ('received "%s"' % data)

            if data == "enable":
                print ('sending data back to the client')
                variables.habilitar_puerta = True
                print ("variables.habilitar_puerta %s" % variables.habilitar_puerta)
                #self.habilitar_puerta = True
                connection.sendall(data)

            elif data == "disable":
                print ('sending data back to the client')
                #self.habilitar_puerta = False
                variables.habilitar_puerta = False
                print ("variables.habilitar_puerta %s" % variables.habilitar_puerta)
                connection.sendall(data)

            else:
                connection.sendall(data)
                print ('no more data from', client_address)

        finally:
            # Clean up the connection
            connection.close()
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()

    def start_service(self):

        # star opendoor service
        # thread.start_new_thread(self.open_door_service, ())
        # Listen for incoming connections
        while True:
            try:
                sys.exc_clear()
                sys.exc_traceback = sys.last_traceback = None
                gc.collect()
                self.sock.listen(1)
                print ('waiting for a connection')
                connection, client_address = self.sock.accept()
                thread.start_new_thread(self.on_new_client, (connection, client_address))
            except:
                self.sock.close()
                sys.exc_clear()
                sys.exc_traceback = sys.last_traceback = None
                gc.collect()
                print ("there was an exception")
                break
