from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.setupUi()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self.hide )
        self.timer.setSingleShot( False )

    def setupUi(self):
        self.dialog.setObjectName("dialog")
        self.dialog.resize(456, 151)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/avatar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialog.setWindowIcon(icon)
        self.image = QtWidgets.QLabel(self.dialog)
        self.image.setGeometry(QtCore.QRect(10, 10, 128, 128))
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("images/warning.png"))
        self.image.setObjectName("image")
        self.msg = QtWidgets.QLabel(self.dialog)
        self.msg.setGeometry(QtCore.QRect(160, 40, 281, 61))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(75)
        self.msg.setFont(font)
        self.msg.setText("")
        self.msg.setObjectName("msg")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("dialog", "Facial Recognition System by MBPO"))

    def show(self,msg):
        msg_type,msg = msg.split(':')
        if msg_type == '0':
            self.image.setPixmap(QtGui.QPixmap("images/warning.png"))
            person,reason = msg.split(',')
            self.msg.setText("¡PERMISO DENEGADO! para " + person + "\nMotivo:\n" + reason)
            font = QtGui.QFont()
            font.setBold(False)
            self.msg.setFont(font)
        elif msg_type == '1':
            self.image.setPixmap(QtGui.QPixmap("images/checked.png"))
            font = QtGui.QFont()
            font.setBold(True)
            font.setPointSize(25)
            self.msg.setFont(font)
            if msg == 'entrance':
                self.msg.setText("¡Bienvenido!")
            elif msg == 'exit':
                self.msg.setText("¡Hasta pronto!")
        self.dialog.show()
        self.timer.start(5000)

    def hide(self):
        self.dialog.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_dialog()
    ui.show("1:in")
    sys.exit(app.exec_())
