import socket
import sys
import time
import serial


port = "COM4"
port = "/dev/ttyUSB0"


baud = 115200
ser = serial.Serial(port, baud, timeout=1)

if ser.isOpen():
    print(ser.name + ' is open...')
    time.sleep(3)
    ser.write(b"r")
    ser.close()
else:
    print(ser.name + ' is NOT open...')
#     # open the serial port
# if ser.isOpen():
# 	print(ser.name + ' is open...')
#     time.sleep(3)
#     ser.write(b"r")
#     ser.close()

# import serial
# ser = serial.Serial()
# ser.port = "/dev/ttyS0" # may be called something different
# ser.baudrate = 115200 # may be different
# ser.open()
# if ser.isOpen():
#     ser.write(b"r")