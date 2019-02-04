import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import socket
import sys
import thread
import time
import serial

#port = "/dev/ttyS0"  # en computador face
port = "/dev/ttyUSB0"  # en mv ubuntu del mac
baud = 115200
ser = serial.Serial(port, baud, timeout=1)
if ser.isOpen():
    print(ser.name + ' is open...')
    time.sleep(2)

def open_door(cmd):
    print ("openning door ")
    try:
        ser.write(b"r")
        print ("THE DOOR WAS OPEN AT EMBEDDED DEVICE")
        return True

    except:
        print ("ERROR: THE DOOR WAS NOT OPEN AT EMBEDDED DEVICE")
        return False

#thread.start_new_thread(speak_name_bienvenida, ("Sistema activo!", 0))
cmd = "r"
open_door(cmd)
#print ("waiting 5 seconds")