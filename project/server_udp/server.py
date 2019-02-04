
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
sys.exc_clear()
sys.exc_traceback = sys.last_traceback = None
import variables
from server_socket_puerta import server_habilitar



def open_door(cmd):
    print ("openning door ")
    try:
        ser.write(b"r")
        print ("THE DOOR WAS OPEN AT EMBEDDED DEVICE")
        return True

    except:
        print ("ERROR: THE DOOR WAS NOT OPEN AT EMBEDDED DEVICE")
        return False

def write_report(name, other):
    folder_path = "/root/openface/demos/web/project/reporte_de_entrada/reportes"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    name_file = time.strftime("%d_%m_%Y") + ".pkl"
    file_path = os.path.join(folder_path, name_file)
    print ("writing name to file %s" % (file_path + "/" + name))

    with open(file_path, "a+") as f:
        f.write(name + "\n")
    return

def speak_name_bienvenida(name, othr):

    tts = gTTS(text="Bienvenido," + name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")

def speak_des_hablitar(name, othr):

    print ("speak_name_bienvenida")
    tts = gTTS(text=name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")

def habilitar_puerta_service():
    server_habilitar_p = server_habilitar.server_habilitar_puerta()
    server_habilitar_p.start_service()
    pass



habilitar_puerta = False
open_door_flag = False
door_bussy = False
name = ""

def open_door_service():
    print ("openning door service start")
    global open_door_flag, name, door_bussy
    while True:
        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()
        #print ("open_door_flag %s" %open_door_flag)

        hora = dt.datetime.now().hour
        if hora <= 16:
            if habilitar_puerta == True:
                if open_door_flag == True:
                    open_door_flag = False
                    door_bussy = True

                    # writing the name to file-report
                    # thread.start_new_thread(write_report, (name, 0))
                    #save_new_data_to_report(name)

                    # speak name
                    thread.start_new_thread(speak_name_bienvenida, (name, 0))

                    # open door
                    cmd = "r"
                    open_door(cmd)
                    print ("waiting 5 seconds")
                    time.sleep(5)
                    print ("waiting done")
                    print ("door closed")

                    name = ""
                    door_bussy = False

port = "/dev/ttyS0"  # en computador face
port = "/dev/ttyUSB0"  # en mv ubuntu del mac
baud = 115200
ser = serial.Serial(port, baud, timeout=1)
if ser.isOpen():
    print(ser.name + ' is open...')
time.sleep(2)


# star opendoor service
#thread.start_new_thread(open_door_service, ())

#start server habilitar puerta
#thread.start_new_thread(habilitar_puerta_service, ())

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print ( 'starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    global open_door_flag, door_bussy, name
    try:
        print ('\nwaiting to receive message')
        data, address = sock.recvfrom(32)

        print ('received %s bytes from %s' % (len(data), address))
        print (sys.stderr, data)

        print ("data %s" %data)

        op = data.split("/")[0]
        if op == "open_door" and door_bussy == False:
            open_door_flag = True
            name = data.split("/")[-1]

        elif op == "enable":
            habilitar_puerta = True


        elif op == "disable":
            habilitar_puerta = False


        sent = sock.sendto(data, address)
        print ( 'sent %s bytes back to %s' % (sent, address))
    except:
        print('closing socket')
        sock.close()
        break


