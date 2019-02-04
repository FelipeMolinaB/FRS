# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import numpy as np
import socket
import cv2
from dialog import Ui_dialog
import glob

IP_SERVER = "localhost"
PORT_SERVER_IM = 7004
PORT_SERVER_INF = 7005

HEIGHT_FACTOR = 411/480
WIDTH_FACTOR = 530/640

class Ui_MainWindow(object):
    def __init__(self,branch_name = "-"):
        self.branch = branch_name
        self.waiting = False
        self.timer = Timer()
        self.image_receiver = ImageReceiver()
        self.info_receiver = InfoReceiver()
        self.timer.update.connect(self.waiting_state)
        self.image_receiver.update_image.connect(self.refresh_image)
        self.image_receiver.update_image.connect(self.timer.event)
        self.info_receiver.update_info.connect(self.refresh_info)
        self.timer.start()
        self.image_receiver.start()
        self.info_receiver.start()
        self.dialog = Ui_dialog()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 480)
        MainWindow.setMinimumSize(QtCore.QSize(812, 480))
        MainWindow.setMaximumSize(QtCore.QSize(812, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/avatar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(10, 30, 530, 411))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("images/Init.jpg"))
        self.image.setObjectName("image")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(550, 30, 241, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.department = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.department.setObjectName("department")
        self.verticalLayout.addWidget(self.department)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.branch_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.branch_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.branch_name.setObjectName("branch_name")
        self.verticalLayout.addWidget(self.branch_name)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 440, 100, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(610, 460, 121, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Facial Recognition System by MBPO"))
        self.label_2.setText(_translate("MainWindow", "NOMBRE:"))
        self.name.setText(_translate("MainWindow", "-"))
        self.label_4.setText(_translate("MainWindow", "AREA/CAMPAÑA:"))
        self.department.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "SEDE:"))
        self.branch_name.setText(_translate("MainWindow", self.branch))
        self.label.setText(_translate("MainWindow", "powered by:"))
        self.label_3.setText(_translate("MainWindow", "MILLENIUM BPO"))

    def refresh_image(self,image):
        self.waiting = False
        image = cv2.resize(image, None, fx=WIDTH_FACTOR, fy=HEIGHT_FACTOR, interpolation=cv2.INTER_LINEAR)
        self.image.setPixmap(QtGui.QPixmap(QtGui.QImage(image, image.shape[1],image.shape[0],3*image.shape[1],QtGui.QImage.Format_RGB888)))

    def refresh_info(self,data):
        msg_type,info = data.split(':')
        if msg_type == '3':
            self.dialog.hide()
        else:
            if not self.waiting:
                if msg_type == '0':
                    self.dialog.show(data)
                elif msg_type == '1':
                    info = info.split(",")
                    self.name.setText(info[0])
                    self.department.setText(info[1])
                elif msg_type == '2':
                    self.dialog.show("1:"+info)

    def waiting_state(self,timeout):
        self.waiting = True
        self.image.setPixmap(QtGui.QPixmap("images/NoPersonDetected.jpg"))
        self.name.setText("-")
        self.department.setText("-")

class ImageReceiver(QtCore.QThread):
    update_image = QtCore.pyqtSignal(np.ndarray)
    update_time = QtCore.pyqtSignal(bool)
    def __init__(self):
        super(ImageReceiver, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (IP_SERVER, PORT_SERVER_IM)
        self.socket.bind(self.server_address)
        self.socket.listen(len(glob.glob("/dev/video*")))

    def run(self):
        print("Image receiver ready")
        while True:
            connection, client_address = self.socket.accept()
            try:
                image = b''
                while(True):
                    data = connection.recv(1024)
                    sent = connection.sendall(b'1')
                    if data == b'\xa5'*1024:
                        break
                    else:
                        image += data
                image = np.frombuffer(image,dtype=np.uint8).reshape((480,640,3))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.update_image.emit(image)
                self.update_time.emit(True)

            # except socket.error:
            #     pass
            except:
                sent = connection.sendall(b'')
                raise
            finally:
                connection.close()

class InfoReceiver(QtCore.QThread):
    update_info = QtCore.pyqtSignal(str)
    def __init__(self):
        super(InfoReceiver, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (IP_SERVER, PORT_SERVER_INF)
        self.socket.bind(self.server_address)
        self.socket.listen(1)

    def run(self):
        print("Info receiver ready")
        while True:
            connection, client_address = self.socket.accept()
            try:
                data = connection.recv(1024)
                self.update_info.emit(data.decode("utf-8"))
                sent = connection.sendall(b'1')
            except:
                sent = connection.sendall(b'')
                raise
            finally:
                connection.close()

class Timer(QtCore.QThread):
    update = QtCore.pyqtSignal(bool)
    def __init__(self):
        super(Timer, self).__init__()
        self.timeout = 2
        self.last_msg = time.time()

    def run(self):
        print("Timer is running")
        while True:

            if time.time()-self.last_msg > 2:
                self.update.emit(True)
            else:
                pass
            time.sleep(0.05)

    def event(self):
        self.last_msg = time.time()

if __name__ == "__main__":
    import sys
    branch_name = "-"
    try:
        cmd = None
        value = None
        if len(sys.argv[1:])>1:
            for arg in sys.argv[1:]:
                if cmd is None:
                    cmd = arg.lower()
                else:
                    if cmd == "-b":
                        branch_name = arg
                        cmd = None
                    else:
                        print("ERROR: Invalid command '{}'".format(cmd))
                        exit()
    except Exception as e:
        raise

    app = QtWidgets.QApplication([sys.argv[0]])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(branch_name)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
