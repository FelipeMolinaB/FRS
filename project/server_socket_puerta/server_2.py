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
sys.exc_clear()
sys.exc_traceback = sys.last_traceback = None


FILE_PATH  = "/media/sf_face_computer_backup/app_face_dlib/project/reporte_de_entrada"

def save_new_data_to_report(name):


    folder_path = FILE_PATH
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "reporte.pkl")

    reporte = joblib.load(file_path)

    time_entrance = time.strftime("%H:%M:%S")
    date_entrance = time.strftime("%d/%m/%Y")
    dato = [date_entrance, time_entrance, name]

    reporte.append(dato)

    joblib.dump(reporte, file_path)



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
    print ("openning door ")
    try:
        ser.write(b"r")
        print ("THE DOOR WAS OPEN AT EMBEDDED DEVICE")
        return True

    except:
        print ("ERROR: THE DOOR WAS NOT OPEN AT EMBEDDED DEVICE")
        return False

def file_creation_first_time():
    folder_path = "/root/openface/demos/web/project/reporte_de_entrada"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "reporte.pkl")

    reporte = []
    time_entrance = time.strftime("%H:%M:%S")
    date_entrance = time.strftime("%d/%m/%Y")
    dato = [date_entrance, time_entrance, "test"]

    reporte.append(dato)

    joblib.dump(reporte, file_path)


def read_report_entrance():
    folder_path = "/root/openface/demos/web/project/reporte_de_entrada"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "reporte.pkl")

    reporte = joblib.load(file_path)

    for report in reporte:
        print (report)


# Create a TCP/IP socket
# Bind the socket to the port
#server_address = ('192.168.56.104', 7001)
server_address = (variables.IP_SERVER, variables.PORT_SERVER)
print ('starting up on %s port %s' % server_address)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)

open_door_flag = False
door_bussy = False
name = ""

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


    tts = gTTS(text="Bienvenido,"+ name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")


def speak_des_hablitar(name, othr):

    print ("speak_name_bienvenida")
    tts = gTTS(text=name, lang='es')
    tts.save("bienvenido.mp3")
    os.system("mpg321 bienvenido.mp3")


def open_door_service():
    print ("openning door service start")
    global open_door_flag, name, door_bussy
    while True:
        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()

        hora = dt.datetime.now().hour
        if hora <= 17:
            if habilitar_puerta == True:
                if open_door_flag == True:
                    door_bussy = True

                    # writing the name to file-report
                    #thread.start_new_thread(write_report, (name, 0))
                    save_new_data_to_report(name)

                    # speak name

                    thread.start_new_thread(speak_name_bienvenida,(name, 0))

                    #open door
                    cmd = "r"
                    open_door(cmd)
                    print ("waiting 5 seconds")
                    time.sleep(5)
                    print ("waiting done")
                    print ("door closed")
                    open_door_flag = False
                    name = ""
                    door_bussy= False




def on_new_client(connection,client_address):
    global open_door_flag, habilitar_puerta, name
    try:
        print ('connection from', client_address)

        # Receive the data in small chunks and retransmit it

        total_data = connection.recv(1024)
        print ('received "%s"' % total_data)
        #if data == "close_server_socket":


        data = total_data.split("/")[0]
        if data == "open_door":
            if door_bussy == False:
                print ('sending data back to the client')
                connection.sendall(data)
                name = total_data.split("/")[-1]
                open_door_flag = True

        elif data == "enable":

            print ('sending data back to the client')
            #thread.start_new_thread(speak_des_hablitar, ("Puerta Habilitada", 0))

            connection.sendall(data)
            habilitar_puerta = True


        elif data == "disable":
            print ('sending data back to the client')
            #thread.start_new_thread(speak_des_hablitar, ("Puerta Deshabilitada", 0))
            connection.sendall(data)
            habilitar_puerta = False


        else:
            connection.sendall(data)
            print ('no more data from', client_address)

    finally:
        # Clean up the connection
        connection.close()
        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()


# star opendoor service
thread.start_new_thread(open_door_service, ())
# Listen for incoming connections
while True:
    try:
        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()

        #save_new_data_to_report(name)

        sock.listen(1)
        print ('waiting for a connection')
        connection, client_address = sock.accept()
        thread.start_new_thread(on_new_client, (connection, client_address))
    except:
        sock.close()
        sys.exc_clear()
        sys.exc_traceback = sys.last_traceback = None
        gc.collect()
        print ("there was an exception")
        break
