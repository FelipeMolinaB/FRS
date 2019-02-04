
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import socket
import sys
import thread
import time
import serial

import datetime as dt
from gtts import gTTS
import os
from threading import Thread
from multiprocessing import Process
from sklearn.externals import joblib
import gc
import sys
import time
import socket
import sys

import variables
from server_socket_puerta import server_habilitar





def write_report(name, other):
    folder_path = "/root/openface/demos/web/project/reporte_de_entrada/reportes"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    name_file = time.strftime("%d_%m_%Y") + ".pkl"
    file_path = os.path.join(folder_path, name_file)
    #print ("writing name to file %s" % (file_path + "/" + name))

    with open(file_path, "a+") as f:
        f.write(name + "\n")
    return

def speak_name_bienvenida(name, othr):

    tts = gTTS(text="Bienvenido," + name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")

def speak_des_hablitar(name, othr):
    #print ("speak_name_bienvenida")
    tts = gTTS(text=name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")

def habilitar_puerta_service():
    server_habilitar_p = server_habilitar.server_habilitar_puerta()
    server_habilitar_p.start_service()




#habilitar_puerta = False
#open_door_flag = False
#door_bussy = False
#name = ""



def open_door_service():
    #global habilitar_puerta, open_door_flag, door_bussy, name
    #port = "/dev/ttyS0"
    port = "/dev/ttyUSB0"
    baud = 115200
    ser = serial.Serial(port, baud, timeout=1)
    if ser.isOpen():
        print(ser.name + ' is open...')
        time.sleep(2)

    def open_door(cmd):
        #print ("openning door ")
        try:
            ser.write(b"r")
            print ("THE DOOR WAS OPEN AT EMBEDDED DEVICE")
            return True

        except:
            print ("ERROR: THE DOOR WAS NOT OPEN AT EMBEDDED DEVICE")
            return False

    thread.start_new_thread(speak_name_bienvenida, ("Sistema activo!", 0))
    cmd = "r"
    open_door(cmd)
    #print ("waiting 5 seconds")
    time.sleep(5)
    #print ("waiting done")
    #print ("door closed")
    #print ("openning door service start")

    #print ("recibiendo peticiones para abrir la puerta")
    while True:
        #print ("variables.open_door_flag %s" %variables.open_door_flag)
        #print ("variables.name %s" %variables.name)

        #print ("open_door_flag %s" %open_door_flag)
        #print ("variables.habilitar_puerta %s" %variables.habilitar_puerta)
        hora = dt.datetime.now().hour
        if hora <= 16 and hora >= 7:
            if variables.habilitar_puerta == True:
                if variables.open_door_flag == True:
                    variables.open_door_flag = False
                    variables.door_bussy = True

                    # writing the name to file-report
                    # thread.start_new_thread(write_report, (name, 0))
                    #save_new_data_to_report(name)

                    # speak name
                    thread.start_new_thread(speak_name_bienvenida, (variables.name, 0))

                    # open door
                    cmd = "r"
                    open_door(cmd)
                    print ("opening door, waiting 5 seconds")
                    time.sleep(5)
                    #print ("waiting done")
                    #print ("door closed")

                    variables.name = ""
                    variables.door_bussy = False
                    sys.exc_clear()
                    sys.exc_traceback = sys.last_traceback = None
                    gc.collect()
        else:
            variables.habilitar_puerta = False


# star opendoor service
#thread.start_new_thread(open_door_service, ())



# Create a UDP socket

def start_server_udp():
    #global habilitar_puerta, open_door_flag, door_bussy, name

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    #server_address = ('localhost', variables.PORT_SERVER_UDP)
    server_address = (variables.IP_SERVER_UDP, variables.PORT_SERVER_UDP)

    print ( 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    cont_person = 0
    last_person = None
    array_person = []


    while True:

        try:
            #print ('\nwaiting to receive message')
            data, address = sock.recvfrom(32)

            #print ('received %s bytes from %s' % (len(data), address))
            #print (sys.stderr, data)

            #print ("data %s" %data)

            op = data.split("/")[0]
            #print ("operation %s" %op)
            if op == "open_door" and variables.door_bussy == False:
                variables.open_door_flag = True
                variables.name = data.split("/")[-1]


                # if cont_person == 0:
                #     last_person = data.split("/")[-1]
                #     cont_person = cont_person + 1
                # else:
                #     if last_person == data.split("/")[-1]:
                #         cont_person = cont_person + 1
                #         if cont_person == variables.n_verificacion:
                #             variables.open_door_flag = True
                #             variables.name = data.split("/")[-1]
                #             cont_person = 0
                #             last_person = None
                #     else:
                #         cont_person = 0
                #         last_person = None



            sent = sock.sendto(data, address)
            #print ( 'sent %s bytes back to %s' % (sent, address))
        except:
            print('closing udp socket')
            sock.close()
            break

        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()


def star_server_tcp():
    #server_address = ('192.168.56.108', variables.PORT_SERVER_TCP)
    server_address = (variables.IP_SERVER_TCP, variables.PORT_SERVER_TCP)
    # server_address = (variables.IP_SERVER, variables.PORT_SERVER)
    print ('starting up tcp server on %s port %s' % server_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    # self.habilitar_puerta = False

    def on_new_client(connection, client_address):
        global open_door_flag, habilitar_puerta, name
        try:
            #print ('connection from', client_address)

            # Receive the data in small chunks and retransmit it

            data = connection.recv(16)
            #print ('received "%s"' % data)

            if data == "enable":
                #print ('sending data back to the client')
                variables.habilitar_puerta = True
                #print ("variables.habilitar_puerta %s" % variables.habilitar_puerta)
                #self.habilitar_puerta = True
                connection.sendall(data)

            elif data == "disable":
                #print ('sending data back to the client')
                #self.habilitar_puerta = False
                variables.habilitar_puerta = False
                #print ("variables.habilitar_puerta %s" % variables.habilitar_puerta)
                connection.sendall(data)

            else:
                connection.sendall(data)
                #print ('no more data from', client_address)

        finally:
            # Clean up the connection
            connection.close()
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()

    while True:
        try:
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            sock.listen(1)
            print ('TCP waiting for a connection')
            connection, client_address = sock.accept()
            thread.start_new_thread(on_new_client, (connection, client_address))
        except:
            sock.close()
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            print ("closing tcp server")
            break




# start opendoor service
thread.start_new_thread(open_door_service, ())
#time.sleep(7)

# start server udp
thread.start_new_thread(start_server_udp, ())

#start server habilitar puerta
thread.start_new_thread(star_server_tcp, ())




while True:

    try:
        pass
    except:
        break

