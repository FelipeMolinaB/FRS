#from tkinter import *
#from tkinter import ttk
import recepcion_utilities
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import Tkinter as tki
from Tkinter import *
import ttk
import tkMessageBox
import client_recepcion

from server_udp import client

def habilitar():
    message = "enable"
    try:
        data_received = client_recepcion.set_door_mode("enable")
        #data_received = client.send_data_to_udp_server(message, server_address=("192.168.56.108", 10000))
        if data_received == message:
            tkMessageBox.showinfo("Respuesta", "Puerta Habilitada")
        else:
            tkMessageBox.showinfo("Respuesta", "La puerta no fue habilitada")
    except:
        tkMessageBox.showinfo("Respuesta", "No se pudo conectar con Server-Door. Contactese con el administrador")


def deshabilitar():
    message = "disable"
    try:
        data_received = client_recepcion.set_door_mode("disable")
        #data_received = client.send_data_to_udp_server(message, server_address=("192.168.56.108", 10000))
        if data_received == message:
            tkMessageBox.showinfo("Respuesta", "Puerta Deshabilitada")
        else:
            tkMessageBox.showinfo("Respuesta", "La puerta no fue Deshabilitada")
    except:
        tkMessageBox.showinfo("Respuesta", "No se pudo conectar con Server-Door. Contactese con el administrador")



root = Tk()
root.title("Reconocimiento Facial")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

#feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
#feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Habilitar", command=habilitar).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Deshabilitar", command=deshabilitar).grid(column=3, row=4, sticky=W)

#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Reconocimiento Facial").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Accion").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#feet_entry.focus()
#root.bind('<Return>', calculate)

root.mainloop()