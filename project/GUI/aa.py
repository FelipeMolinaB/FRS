# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FRS.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(812, 480)
        MainWindow.setMinimumSize(QtCore.QSize(812, 480))
        MainWindow.setMaximumSize(QtCore.QSize(812, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/Screenshot from 2018-12-12 08-04-23.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(10, 30, 530, 411))
        self.image.setStyleSheet("background-image: url(:/newPrefix/Screenshot from 2018-12-28 13-12-48.png);")
        self.image.setFrameShape(QtWidgets.QFrame.Box)
        self.image.setLineWidth(2)
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("../../../../.designer/backup/NoPersonDetected.jpg"))
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
        self.label.setGeometry(QtCore.QRect(630, 440, 66, 17))
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
        self.name.setText(_translate("MainWindow", "Juan Felipe Molina Bermudez"))
        self.label_4.setText(_translate("MainWindow", "AREA/CAMPAÑA:"))
        self.department.setText(_translate("MainWindow", "Datos No Estructurados"))
        self.label_6.setText(_translate("MainWindow", "SEDE:"))
        self.branch_name.setText(_translate("MainWindow", "Zuca"))
        self.label.setText(_translate("MainWindow", "power by:"))
        self.label_3.setText(_translate("MainWindow", "MILLENIUM BPO"))

import mmm_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

