#!/usr/bin/python

import time
from sklearn.externals import joblib

print (time.strftime("%H:%M:%S"))
print (time.strftime("%d/%m/%Y"))
import os

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

def save_new_data_to_report(name):

    folder_path = "/root/openface/demos/web/project/reporte_de_entrada"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "reporte.pkl")

    reporte = joblib.load(file_path)

    time_entrance = time.strftime("%H:%M:%S")
    date_entrance = time.strftime("%d/%m/%Y")
    dato = [date_entrance, time_entrance, name]

    reporte.append(dato)

    joblib.dump(reporte,file_path)

def read_report_entrance():
    folder_path = "/media/sf_face_computer_backup/app_face_dlib/project/reporte_de_entrada"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "reporte.pkl")

    reporte = joblib.load(file_path)

    for report in reporte:
        print (report)


#file_creation_first_time()
#save_new_data_to_report("test")
read_report_entrance()