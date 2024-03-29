# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent
from gestor import users_gestor, wares_gestor
from datetime import datetime
from ware_dialog import Ui_Dialog
import threading
import time

enable_datetime = True


#class Ui_MainWindow(object):
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data_user = None, data_ware = None, usr_text = "", ware_text = "", parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        """**data_ware y data_user = (objectCODE, objects(List), Permisos)"""
        self.ware_name = ware_text
        """TODO DE USUARIO"""
        self.usr_text = usr_text
        """TODO DE WARES"""
        #NOS QUEDAMOS EN ESTA PARTE
        self.dialog = QDialog()
        self.ui_dialog = Ui_Dialog(data_user, data_ware, self.dialog)
        self.setupUi()
        #self.ui_dialog.init_condition()

    #def setupUi(self, MainWindow):
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 1024)
        self.setFixedSize(1280, 1024)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1280, 100))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.user_label = QtWidgets.QLabel(self.frame)
        self.user_label.setGeometry(QtCore.QRect(1060, 20, 191, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.user_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.user_label.setFont(font)
        self.user_label.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.user_label.setObjectName("user_label")


        self.ware_labe = QtWidgets.QLabel(self.frame)
        self.ware_labe.setGeometry(QtCore.QRect(780, 60, 255, 31))
        self.ware_labe.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ware_labe.setFont(font)
        self.ware_labe.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.ware_labe.setObjectName("ware_labe")


        self.date_label = QtWidgets.QLabel(self.frame)
        self.date_label.setGeometry(QtCore.QRect(1060, 60, 191, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.date_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.date_label.setFont(font)
        self.date_label.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.date_label.setObjectName("date_label")
        # -----------  warelabel cofiguration  -----------

        self.ware_label = QtWidgets.QLabel(self.frame)
        self.ware_label.setGeometry(QtCore.QRect(30, 15, 72, 72))
        self.ware_label.setText("")
        self.ware_label.setPixmap(QtGui.QPixmap("C:/Users/IROJAS/Desktop/Genesis/UI_STNG/imgs/warehouse_icon.png"))
        self.ware_label.setScaledContents(True)
        self.ware_label.setObjectName("ware_label")
        self.ware_label.mousePressEvent = self.open_wareWindow


        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 737, 1280, 287))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("imgs/main_window_button.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.notification_table = QtWidgets.QTableWidget(self.centralwidget)
        self.notification_table.setEnabled(False)
        self.notification_table.setGeometry(QtCore.QRect(0, 120, 1280, 617))
        self.notification_table.setObjectName("notification_table")
        self.notification_table.setColumnCount(3)
        self.notification_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(2, item)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 100, 1280, 20))
        self.frame_2.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.run_threads()

    def open_wareWindow(self, event):
        self.ui_dialog.init_condition()
        self.setEnabled(False)
        self.ui_dialog.show_window()
        if self.ui_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.setEnabled(True)

    def update_datetime(self):
        while(enable_datetime):
            self.date_label.setText(datetime.now().strftime("%H:%M %d/%m/%Y"))
            time.sleep(0.5)

    def run_threads(self):
        self.t1 = threading.Thread(target=self.update_datetime)
        self.t1.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Genesis - [Museo del Libro]"))
        self.user_label.setText(_translate("MainWindow", "USER: " + self.usr_text.upper()))
        self.date_label.setText(_translate("MainWindow", "18:39 20/04/2021"))
        self.ware_labe.setText(_translate("MainWindow", "ALMACEN: " + self.ware_name.upper()))
        self.ware_labe.adjustSize() #Ajusta el tamaño del label al tamaño de las letras
        self.ware_labe.move(1040 - self.ware_labe.width(),66) #cambia la posicion del label

        item = self.notification_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "N°"))
        item = self.notification_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Notificación"))
        item = self.notification_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Estado"))


class Ui_LoginWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None): #para que puse el parent = None?
        super(Ui_LoginWindow, self).__init__(parent)
        #se crea el gestor de almacenes
        self.user_gest = users_gestor()
        self.ware_gest = wares_gestor()
        #self.user_gest.fill_users()

    def openMainWindow(self):
        #param1 es bool para existencia de usuario, param2 para ver usuario habilitado bool
        param1, data_user = self.user_gest.check_login(self.lineEdit.text(),self.lineEdit_2.text())
        # ware_exist is bool, ware_abrev is real name of ware, abrev is abreviation of ware
        self.ware_exist, data_ware, ware_name  = self.ware_gest.exist_ware()

        #lineEdit = usr, lineEdit_2 = passwd ???

        if param1 and self.ware_exist and data_user[2] and data_ware[2][0] == True:
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_MainWindow(data_user, data_ware, self.lineEdit.text(), ware_name)
            LoginWindow.close()
            self.ui.show()

        elif param1 and self.ware_exist and data_user[2] and data_ware[2][0] == False:
            self.label_message.setVisible(False)
            QMessageBox.about(self, "Alerta", "El almacen esta desabilitado")

        elif param1 == True and self.ware_exist == False and data_user[2] == True:
            self.label_message.setVisible(False)
            QMessageBox.about(self, "Alerta", "La computadora no tiene registro")

        elif param1 == True and self.ware_exist == False and data_user[2] == False:
            self.label_message.setVisible(False)
            QMessageBox.about(self, "Alerta", "*La computadora no tiene registro\n*La cuenta del usuario esta desactivada")

        elif param1 == True and self.ware_exist == True and data_user[2] == False:
            self.label_message.setVisible(False)
            QMessageBox.about(self, "Alerta", "La cuenta del usuario esta desactivada")

        elif param1 == False and self.ware_exist == True and data_user[2] == False:
            self.label_message.setVisible(True)

        elif param1 == False and self.ware_exist == False and data_user[2] == False:
            self.label_message.setVisible(True)
        else:
            self.label_message.setVisible(True)

    # -----------  evento enter  -----------
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and
            (source is self.lineEdit_2 or source is self.lineEdit)):
            
            if event.text() == "\r":
                self.openMainWindow()
            #print('key press:', (event.key(), event.text()))
        return super(Ui_LoginWindow, self).eventFilter(source, event)

    def setupUi(self, LoginWindow):

        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(380, 312)
        LoginWindow.setFixedSize(380,312)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")

        # -----------  Login Button  -----------
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(70, 240, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)

        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("background-color: rgb(189, 189, 189);\n"
"")
        self.pushButton.setIconSize(QtCore.QSize(300, 50))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openMainWindow)
        # ======  End of Login Button  =======
        
        # -----------  lineEdit_1  -----------
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(70, 110, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setMaxLength(8)
        self.lineEdit.setFrame(True)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.installEventFilter(self) # metodo para llamar a funcion keypressed
        

        # ======  End of lineEdit_1  =======
        
        # -----------  lineEdit_2  -----------
        
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 170, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(8)
        self.lineEdit_2.setFrame(True)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.installEventFilter(self) #metodo para llamar a funcion keypressed
        # ======  End of lineEdit_2  =======
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(55, 30, 270, 54))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("C:/Users/IROJAS/Desktop/Genesis/UI_STNG/imgs/login_user.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # -----------  wrongLogin label  -----------
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(65)

        self.label_message = QtWidgets.QLabel(self.centralwidget)
        self.label_message.setPalette(palette)
        self.label_message.setGeometry(QtCore.QRect(70, 195, 250, 54))
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("")
        self.label_message.setText("Usuario o contraseña incorrecta")
        self.label_message.setObjectName("label_message")
        self.label_message.setVisible(False)

        # ======  End of wrongLogin label   =======
        
        
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(LoginWindow)
        self.statusbar.setObjectName("statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Genesis - [Museo del Libro]"))
        self.pushButton.setText(_translate("LoginWindow", "Log in"))
        self.lineEdit.setPlaceholderText(_translate("LoginWindow", "User"))
        self.lineEdit_2.setPlaceholderText(_translate("LoginWindow", "Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    app.exec_()
    enable_datetime = False

