# coding=utf-8
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import socket
import serial

import datetime as dt
from threading import Thread, Timer
from sklearn.externals import joblib
import gc
import time
import psycopg2

import variables
import glob

WAIT_TIME = 5

class FRSServer(object):
    def __init__(self, branch_id = 0, in_out_control = True, baudrate = 115200):
        ports = glob.glob('/dev/ttyUSB*')
        print("Serial Ports Available: {}".format(",".join(ports)))
        self.ser = None
        for port in ports:
            try:
                self.ser = serial.Serial(port = port,baudrate = baudrate)
                self.ser.flush()
                if self.ser.isOpen():
                    msg = self.ser.readline().strip()
                    if msg == "This is the turnstile controller":
                        self.ser.write("\n")
                        break
            except:
                raise
                if isinstance(self.ser,serial.Serial):
                    if self.ser.isOpen():
                        self.ser.close()
                self.ser = None
        if self.ser is None:
                print("[{}] Unable to connect with Arduino".format(dt.datetime.now()))
                exit()
        else:
            print("[{}] Connected with the turnstile controller over port {}".format(dt.datetime.now(),port))
            self.ser.flush()
            time.sleep(2)
        self.cc = None
        self.direction = None
        self.is_enable = None
        self.release_access = False
        self.access_busy = False
        self.command_OK = False
        self.no_person_detected_at = []
        self.available_cams = 0
        self.wait_for_a_valid_person = True
        self.permission_denied = None
        self.branch_id = branch_id
        self.in_out_control = in_out_control
        self.face_ratio = None
        self.active_camera = None
        self.users =  dict()
        self.info = None
        self.timer = Timer(WAIT_TIME,self.timeout)
        self.was_set = False
        self.main()

    def send_cmd(self,cmd):
        while(True):
            try:
                if not self.access_busy and not(self.command_OK):
                    self.ser.write(cmd)
                    print ("[{}] Command sent: \"{}\"".format(dt.datetime.now(),cmd.strip()))
                    for i in range(10):
                        if self.command_OK:
                            self.command_OK = False
                            return True
                        time.sleep(0.05)
                    print ("[{}] Timeout for command confirmation".format(dt.datetime.now()))

            except Exception as e:
                raise
                print ("[{}] Command sent: \"{}\" couldn't be sent".format(dt.datetime.now(),cmd.strip()))
            return False

    def access_feedback(self):
        try:
            while True:
                msg = self.ser.readline().strip()
                msg = msg.split()

                if msg[0] == "-b":
                    self.access_busy = bool(int(msg[1]))
                    if self.access_busy:
                        print("[{}] Turnstile is busy".format(dt.datetime.now()))
                    else:
                        print("Turnstile is not busy")
                        self.send_msg_over_socket("3:")
                elif msg[0] == "-c":
                    self.command_OK = bool(int(msg[1]))
                    if self.command_OK:
                        print ("[{}] The command has been confirmed".format(dt.datetime.now()))
                    else:
                        print("ERROR: Invalid command")
                        exit()
        except:
            raise

    def access_controler(self):
        try:
            while True:
                hour = dt.datetime.now().hour
                if hour >= 6 and hour < 16:
                    if not(self.is_enable) or self.is_enable is None:
                        self.is_enable = True
                        cmd = "-t 1\n" #turn on
                        if self.send_cmd(cmd):
                            print("[{}] FRS has been turn on".format(dt.datetime.now()))
                        else:
                            print("[{}] Unable to turn on the FRS".format(dt.datetime.now()))
                    else:
                        if self.release_access and not self.access_busy:
                            self.release_access = False

                            cmd = "-r "
                            print(self.direction)
                            if self.direction == "entrance":
                                cmd += "i" #release in entrance direction
                                print("[{}] La persona identificada con C.C. {} ingreso.".format(dt.datetime.now(),str(self.cc)))
                            elif self.direction == "exit":
                                cmd += "o" #release in exit direction
                                print("[{}] La persona identificada con C.C. {} salio.".format(dt.datetime.now(),str(self.cc)))
                            else:
                                continue
                            cmd += "\n"
                            self.send_cmd(cmd)
                            while not self.access_busy:
                                time.sleep(0.1)

                            if self.in_out_control:
                                self.log_access(self.cc,self.direction)

                            self.send_msg_over_socket("2:"+self.direction)

                            self.direction = None
                            self.face_ratio = None
                            self.was_set = False
                            # self.access_busy = True
                            # print ("Releasing door, waiting 5 seconds")
                            # time.sleep(5)
                            # self.access_busy = False

                            sys.exc_clear()
                            sys.exc_traceback = sys.last_traceback = None
                            gc.collect()

                        elif not(self.permission_denied is None) and not self.access_busy:
                            self.permission_denied = None
                            cmd = "-p "
                            if self.direction == "entrance":
                                cmd += "i" #pd in entrance direction
                                print("[{}] La persona identificada con C.C. {} no tiene permisos de ingreso\n\tMotivo:{}.".format(dt.datetime.now(),self.cc,self.permission_denied))
                            elif self.direction == "exit":
                                cmd += "o" #pd in exit direction
                                print("[{}] La persona identificada con C.C. {} no tiene permisos de salida\n\tMotivo:{}.".format(dt.datetime.now(),self.cc,self.permission_denied))
                            cmd += "\n"
                            self.send_cmd(cmd)
                            while not self.command_OK:
                                pass

                            sql = """SELECT nombre,apellido FROM reconocimiento_facial.personas WHERE cedula = {} ;""".format(self.cc)
                            cur.execute(sql)
                            person = cur.fetchone()

                            msg = "0:" + person[0] + ' ' + person[1] + ',' + self.permission_denied
                            if not self.send_msg_over_socket(msg):
                                print("Problem with FSR GUI")

                        # elif not(self.direction is None):
                        #     cmd = "-s "
                        #     if self.direction == "entrance":
                        #         cmd += "i" #pd in entrance direction
                        #         print("[{}] Se ha detectado una persona valida esperando autorización para entrar.".format(dt.datetime.now()))
                        #     elif self.direction == "exit":
                        #         cmd += "o" #pd in exit direction
                        #         print("[{}] Se ha detectado una persona valida esperando autorización para salir.".format(dt.datetime.now()))
                        #     cmd += "\n"
                        #     self.send_cmd(cmd)
                        #     while not self.command_OK:
                        #         pass
                        #     was_set = True
                        #
                        # elif self.direction is None and was_set:
                        #     cmd = "-t 1\n"
                        #     self.send_cmd(cmd)
                        #     while not self.command_OK:
                        #         pass
                        #     was_set = False
                else:
                    if self.is_enable or self.is_enable is None:
                        self.is_enable = False
                        print("[{}] Turning off the FRS due to time".format(dt.datetime.now()))
                        cmd = "-t 0\n" #turn off
                        self.send_cmd(cmd)
                    time.sleep(60)
        except:
            raise

    def send_info(self):
        while True:
            if not(self.info is None):
                if self.in_out_control:
                    if self.info != 'UK':
                        sql = """SELECT persona_id,nombre,apellido,area FROM reconocimiento_facial.personas WHERE cedula = {} ;""".format(self.info)
                        cur.execute(sql)
                        person = cur.fetchone()

                        msg = "1:" + person[1] + ' ' + person[2] + ',' + person[3]

                        sql = """SELECT "campaña" FROM reconocimiento_facial.permisos WHERE person_id = {} ;""".format(person[0])
                        cur.execute(sql)
                        campana_id = cur.fetchone()[0]

                        if not( campana_id is None):
                            sql = """SELECT nombre FROM reconocimiento_facial."campañas" WHERE id = {} ;""".format(campana_id)
                            cur.execute(sql)
                            campana = cur.fetchone()[0]

                            msg += '/' + campana

                    else:
                        msg = "1:Desconcido,-"
                else:
                    msg = "1:,"
            else:
                msg = "1:{},Desconocida".format(self.info)
            self.info = None
            if not self.send_msg_over_socket(msg):
                print("Problem with FSR GUI")
                time.sleep(0.05)

    def send_msg_over_socket(self,msg):
        gui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (variables.IP_SERVER_IM, variables.PORT_SERVER_INF)
        data = False
        try:
            gui_socket.connect(server_address)
            sent = gui_socket.sendall(msg.encode())
            data,_ = gui_socket.recvfrom(1024)
            gui_socket.close()
        except Exception as e:
            print(e)
        finally:
            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()
            return bool(data)

    def log_access(self,cc,direction):
        sql = """SELECT persona_id FROM reconocimiento_facial.personas WHERE cedula = {} ;""".format(cc)
        cur.execute(sql)
        person_id = cur.fetchone()[0]

        if direction == "entrance":
            direction = "ENTRADA"
        elif direction == "exit":
            direction = "SALIDA"
        sql = """INSERT INTO reconocimiento_facial.accesos (persona_id,sede, fecha, tipo) VALUES ({},{},'{}',{});""".format(self.branch_id,person_id,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),direction)
        cur.execute(sql)

    def has_permission(self):
        print("[{}] Consultando permisos para la persona identificada con C.C. {}\n\tMotivo:{}.".format(dt.datetime.now(),self.cc,self.permission_denied))
        if self.in_out_control or branch == "DEMO":
            try:
                permission = True
                sql = """SELECT persona_id FROM reconocimiento_facial.personas WHERE cedula = {} ;""".format(self.cc)
                cur.execute(sql)
                person_id = cur.fetchone()[0]

                if self.direction == "entrance":

                    sql = """SELECT * FROM reconocimiento_facial.permisos WHERE persona_id = {} AND sede = {} ;""".format(person_id,self.branch_id)
                    cur.execute(sql)
                    now = dt.datetime.now()
                    datetime_permission = False
                    for permission in cur:
                        if now.strftime("%a") in permission[-1]:
                            if now.time() >= permission[4] and now.time() <= permission[5]:
                                datetime_permission = True
                                break

                    if datetime_permission:
                        permission &= True
                    else:
                        self.permission_denied = "No Datetime permissions."
                        return False

                sql = """SELECT * FROM reconocimiento_facial.accesos WHERE persona_id = {} AND sede = {} ;""".format(person_id,self.branch_id)
                cur.execute(sql)
                last_access = None
                for access in cur:
                    datetime = dt.datetime.strptime(access[3], "%Y-%m-%d %H:%M:%S")
                    try:
                        if datetime.date() == now.date() and  datetime>last_access:
                            last_access = datetime
                    except TypeError:
                        last_access = datetime

                if last_access is None:
                    if self.direction == "entrance":
                        permission &= True
                    else:
                        print("[{}] Se le generara un reporte a la persona identificada con C.C. {} \n\tMotivo:{}.".format(dt.datetime.now(),str(self.cc),"Entry request without a exit log"))
                        permission &= True

                        sql = """SELECT id FROM reconocimiento_facial.tipos_resportes WHERE reporte = 'ENTRADA SIN SALIDA';"""
                        cur.execute(sql)
                        self.generate_report(self.cc,cur.fetchone()[0])
                        """self.permission_denied = "Entry request without a exit log."
                        return False"""
                else:
                    if self.direction == "entrance":
                        if last_access[-1] == "SALIDA":
                            permission &= True
                        else:
                            print("[{}] Se le generara un reporte a la persona identificada con C.C. {} \n\tMotivo:{}.".format(dt.datetime.now(),str(self.cc),"Entry request without a exit log"))
                            permission &= True

                            sql = """SELECT id FROM reconocimiento_facial.tipos_resportes WHERE reporte = 'ENTRADA SIN SALIDA';"""
                            cur.execute(sql)
                            self.generate_report(self.cc,cur.fetchone()[0])
                            """self.permission_denied = "Entry request without a exit log."
                            return False"""
                    else:
                        if last_access[-1] == "ENTRADA":
                            permission &= True
                        else:
                            print("[{}] Se le generara un reporte a la persona identificada con C.C. {} \n\tMotivo:{}.".format(dt.datetime.now(),str(self.cc),"Exit request without a entry log"))
                            permission &= True
                            sql = """SELECT id FROM reconocimiento_facial.tipos_resportes WHERE reporte = 'SALIDA SIN ENTRADA';"""
                            cur.execute(sql)
                            self.generate_report(self.cc,cur.fetchone()[0])
                            """self.permission_denied = "Exit request without a entry log."
                            return False"""

                return permission

            except psycopg2.OperationalError:
                return True
        else:
            return True

    def generate_report(self,cc,type):
        sql = """SELECT persona_id FROM reconocimiento_facial.personas WHERE cedula = {} ;""".format(cc)
        cur.execute(sql)
        person_id = cur.fetchone()[0]

        sql = """INSERT INTO reconocimiento_facial.reportes (sede, persona_id, fecha, tipo) VALUES ({},{},'{}',{});""".format(self.branch_id,person_id,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),type)
        cur.execute(sql)

    def timeout(self):
        self.direction = None
        self.face_ratio = None
        self.active_camera = None
        self.send_cmd("-t 1\n")
        self.was_set = False

    def set_direction(self):
        cmd = "-s "
        if self.direction == "entrance":
            print("[{}] Se ha detectado una persona valida esperando autorización para entrar.".format(dt.datetime.now()))
            cmd += 'i\n'
        elif self.direction == "exit":
            print("[{}] Se ha detectado una persona valida esperando autorización para salir.".format(dt.datetime.now()))
            cmd += 'o\n'
        self.send_cmd(cmd)
        self.was_set = True

    def main(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (variables.IP_SERVER_UDP, variables.PORT_SERVER_UDP)

        print ( 'starting up on %s port %s' % server_address)
        self.sock.bind(server_address)
        self.sock.listen(len(glob.glob('/dev/video*')))

        threads = [Thread(target=self.access_feedback),Thread(target=self.access_controler),Thread(target=self.access_controler)]
        if show_outside:
            threads.append(Thread(target=self.send_info))
        print("Starting all Threads")
        for thread in threads:
            thread.daemon = True
            thread.start()
        print("All threads are running")

        users = dict()
        while True:
            try:
                connection, client_address = self.sock.accept()
                data,_ = connection.recvfrom(1024)
                cam,cc,face_area,face_ratio,direction = data.split("/")
                face_area,face_ratio = float(face_area),float(face_ratio)
                if not(direction in self.users):
                    self.users.update({direction:{}})

                if not(cam in self.users[direction]):
                    self.users[direction].update({cam:{}})
                    self.available_cams += 1
                    print("[{}] New Camara available in {} access point".format(dt.datetime.now(),direction))

                if cc == '':
                    sent = connection.sendall('')
                    continue

                if not self.access_busy:
                    self.info = cc
                    if cc == "UK":
                        if not self.was_set:
                            self.direction = direction
                            self.face_ratio = face_ratio
                            self.active_camera = cam
                            self.timer = Timer(WAIT_TIME,self.timeout)
                            self.timer.start()
                            self.set_direction()
                            sent = connection.sendall('S')
                        else:
                            if direction == self.direction:
                                if self.active_camera == cam:
                                    sent = connection.sendall('S')
                                else:
                                    if face_ratio > self.face_ratio*6/5:
                                        self.face_ratio = face_ratio
                                        self.active_camera = cam
                                        sent = connection.sendall('S')
                                    else:
                                        sent = connection.sendall('')
                    else:
                        if self.timer.isAlive():
                            self.timer.cancel()
                        self.cc = int(cc)
                        self.direction = direction
                        self.face_ratio = face_ratio
                        self.active_camera = cam
                        if not self.release_access:
                            if self.has_permission():
                                self.release_access = True

                else:
                    sent = connection.sendall('')
                # if cc != "UK":
                #     if self.direction is None and self.face_ratio is None:
                #         self.direction = direction
                #         self.face_ratio = face_ratio
                #         self.active_camera = cam
                #         # for dir in self.users:
                #         #     if dir != self.direction:
                #         #         for cam in self.users[dir]:
                #         #             self.users[dir][cam] = {}
                #         sent = connection.sendall('S')
                #     else:
                #         if direction == self.direction:
                #             # if cc in self.users[direction][cam]:
                #             #     self.users[direction][cam][cc]["face_area"] += face_area
                #             #     self.users[direction][cam][cc]["count"] += 1
                #             # else:
                #             #     self.users[direction][cam].update({cc:dict(zip(["face_area","count"],[face_area,0]))})
                #             if self.active_camera == cam:
                #                 sent = connection.sendall('S')
                #             else:
                #                 if face_ratio > self.face_ratio:
                #                     self.face_ratio = face_ratio
                #                     self.active_camera = cam
                #                     sent = connection.sendall('S')
                #                 else:
                #                     sent = connection.sendall('')
                # else:
                #     if not (cc in self.users[direction][cam]):
                #         self.users[direction][cam].update({cc:dict(zip(["face_area","count"],[0,0]))})
                #
                #     if cc == '':
                #         if not cam in self.no_person_detected_at:
                #             self.no_person_detected_at.append(cam)
                #         if len(self.no_person_detected_at) == self.available_cams and not self.wait_for_a_valid_person:
                #             self.wait_for_a_valid_person = True
                #             self.no_person_detected_at = []
                #             self.direction = None
                #             self.face_ratio = None
                #         sent = connection.sendall('S')#('')
                connection.close()

                # keys_to_delete = []
                # for user in self.users[direction][cam]:
                #     print(user,self.users[direction][cam])
                #     if user != cc or user == "UK" or user == '':
                #         keys_to_delete.append(user)
                #
                # for key in keys_to_delete:
                #     del self.users[direction][cam][user]

                # ccs = []
                # flag = True
                # for cameras in self.users[direction]:
                #     for camera in cameras:
                #         if len(self.users[direction][camera]) == 0:
                #             flag = False
                #             self.direction = None
                #             self.face_ratio = None
                #         else:
                #             ccs += self.users[direction][camera].keys()

                # if flag:
                    # self.wait_for_a_valid_person = False
                    # self.no_person_detected_at = []
                    #
                    # print("[{}] People with CCs: {} were recognized in {} direction".format(dt.datetime.now(),"".join(ccs),self.direction))
                    #
                    # if self.is_enable and self.direction == direction and not(self.access_busy):
                    #     users = {}
                    #     for cameras in self.users[self.direction]:
                    #         for camera in cameras:
                    #             for user in self.users[direction][camera]:
                    #                 if user in users:
                    #                     users[user]["face_area"] += self.users[direction][camera][user]["face_area"]
                    #                     users[user]["count"] += self.users[direction][camera][user]["count"]
                    #                 else:
                    #                     users.update({user:self.users[direction][camera][user]})
                    #
                    #     people = []
                    #     for user in users:
                    #         if user["count"] >= variables.n_verificacion:
                    #             people.appen(user)
                    #
                    #     best_option = None
                    #     for person in people:
                    #         try:
                    #             if person["face_area"] > best_option["face_area"]:
                    #                 best_option = person
                    #         except:
                    #             best_option = person
                    #
                    #     if not(best_option is None):
                    #         self.cc = int(best_option.keys())
                    #         if not self.release_access:
                    #             self.direction = None
                    #             self.face_ratio = None
                    #             if self.has_permission():
                    #                 self.release_access = True

                        ## self.cc = int(self.cc)
                        ## if not (self.cc in users[self.active_cam]):
                        ##     users[self.active_cam][self.cc] = 1
                        ## else:
                        ##    users[self.active_cam][self.cc] += 1
                        ##     if users[self.active_cam][self.cc] >= variables.n_verificacion:
                        ##         users[self.active_cam][self.cc] = 0
                        ##         if not self.release_access:
                        ##             self.direction = None
                        ##             self.active_cam = None
                        ##             for camera in users:
                        ##                 users[camera] = {}
                        ##             if self.has_permission():
                        ##                 self.release_access = True
            except:
                print('closing udp socket')
                self.sock.close()
                self.send_cmd("-t 0\n")
                self.ser.close()
                raise
                break

            sys.exc_clear()
            sys.exc_traceback = sys.last_traceback = None
            gc.collect()

if __name__ == "__main__":
    branch = "DEMO"
    in_out_control = True
    show_outside = False
    cmd = None

    try:
        if len(sys.argv[1:])>1:
            for arg in sys.argv[1:]:
                if cmd is None:
                    cmd = arg.lower()
                else:
                    if cmd == "-b":
                        branch = arg
                        cmd = None
                    elif cmd == "-c":
                        in_out_control = bool(int(arg))
                        cmd = None
                    elif cmd == "-so":
                        show_outside = bool(int(arg))
                        cmd = None
                    else:
                        print("ERROR: Invalid command '{}'".format(cmd))
                        exit()
    except Exception as e:
        print(e)
    if in_out_control:
        conn = psycopg2.connect("dbname='mineria_datos' user='twitter' host='192.168.73.242' password='twitter' ")
        cur = conn.cursor()

        sql = """SELECT id FROM reconocimiento_facial.sedes WHERE nombre = '{}' ;""".format(branch)
        cur.execute(sql)
        branch_id = cur.fetchone()[0]

        server = FRSServer(branch_id=branch_id,in_out_control=in_out_control)
    else:
        server = FRSServer(in_out_control=in_out_control)
