# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(456, 151)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/aaa/avatar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        self.image = QtWidgets.QLabel(dialog)
        self.image.setGeometry(QtCore.QRect(10, 10, 128, 128))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap(":/aaa/warning.png"))
        self.image.setObjectName("image")
        self.msg = QtWidgets.QLabel(dialog)
        self.msg.setGeometry(QtCore.QRect(160, 40, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.msg.setFont(font)
        self.msg.setText("")
        self.msg.setObjectName("msg")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Facial Recognition System by MBPO"))

import aaa_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

