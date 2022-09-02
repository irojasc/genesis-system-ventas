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
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import QEvent
from gestor import users_gestor, wares_gestor, notifications
from datetime import datetime
from ware_dialog import Ui_Dialog
from sales_Dialog import sales_Dialog
import threading
import time
import pyautogui


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
        self.ownUsers = data_user
        self.ownWares = data_ware
        self.noti_gest = notifications()
        self.notificaciones = []
        # ----- Creas objeto Qdialog para almacen----- #
        self.dialog_ = QDialog()
        self.ui_dialog = Ui_Dialog(data_user, data_ware, self.dialog_)
        # ----- Creas objeto Qdialog para ventas ----- #
        self.dialog = QDialog()
        self.sales_dialog = sales_Dialog(data_user, data_ware, self.dialog)

        self.setupUi()
        self.init_conditions()
        self.isopenware = False
        self.isupdate = False
        self.isupdateWare = False
        #self.ui_dialog.init_condition()

    def doubleClickItem(self, item):
        row = item.row()
        column = item.column()
        cod = int(self.notification_table.item(row, 0).text()[2:]) ##este es el que manda
        ind_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
        if self.noti_gest.trasfer_list[ind_].state == "ABIERTO" and column == 2 and self.noti_gest.trasfer_list[ind_].f_point == self.ownWares[0]:
            text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña", QtWidgets.QLineEdit.Password)
            inde = next((index for (index, d) in enumerate(self.ownUsers[1]) if d.passwd == text_), None) ##index de usuario
            if inde != None and validation_ and not self.isupdate:
                val, usr = self.noti_gest.validarReceiver(cod, self.ownUsers[1][inde].user)
                if val and usr != None:
                    index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
                    self.noti_gest.trasfer_list[index_].receiver = usr
                    self.noti_gest.trasfer_list[index_].state = "ATENDIDO"
                elif not val and usr != None:
                    ret = QMessageBox.question(self, 'Alerta', "Otro usuario esta atendiendo la operación", QMessageBox.Ok, QMessageBox.Ok)
                    index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod),None)
                    self.noti_gest.trasfer_list[index_].receiver = usr
                    self.noti_gest.trasfer_list[index_].state = "ATENDIDO"

        elif self.noti_gest.trasfer_list[ind_].state == "ATENDIDO" and column == 3 and self.noti_gest.trasfer_list[ind_].f_point == self.ownWares[0]:
            ind_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None) #indice de lista back
            button = self.showDialog(self.noti_gest.getText(self.noti_gest.trasfer_list[ind_].items))
            if button == QMessageBox.Yes and not self.isupdate:
                text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña para validar", QtWidgets.QLineEdit.Password)
                inde = next((index for (index, d) in enumerate(self.ownUsers[1]) if d.passwd == text_), None)  ##index de usuario
                if inde != None and validation_ and not self.isupdate and self.ownUsers[1][inde].user == self.noti_gest.trasfer_list[ind_].receiver:
                    bo, date_ = self.noti_gest.ingresarItems(self.ownWares[0], self.noti_gest.trasfer_list[ind_].items, datetime.now().strftime("%Y-%m-%d"), cod)
                    if not bo and date_ != None:
                        index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
                        self.noti_gest.trasfer_list[index_].f_date = str(date_)
                        self.noti_gest.trasfer_list[index_].state = "CERRADO"
                        ret = QMessageBox.question(self, 'Alerta', "La operación ya fue validada!", QMessageBox.Ok, QMessageBox.Ok)
                    elif bo and date_ != None:
                        index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
                        self.noti_gest.trasfer_list[index_].f_date = str(date_)
                        self.noti_gest.trasfer_list[index_].state = "CERRADO"
                        self.isupdateWare = True
                        ret = QMessageBox.question(self, 'Alerta', "Operación validada correctamente!", QMessageBox.Ok, QMessageBox.Ok)

                elif inde != None and validation_ and not self.isupdate and self.ownUsers[1][inde].user != self.noti_gest.trasfer_list[ind_].receiver:
                    ret = QMessageBox.question(self, 'Alerta', "Debe validar el usuario que esta atendiendo", QMessageBox.Ok, QMessageBox.Ok)

            elif not self.isupdate and button == QMessageBox.Abort:
                text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Observación', "Ingrese contraseña para observar operación", QtWidgets.QLineEdit.Password)
                inde = next((index for (index, d) in enumerate(self.ownUsers[1]) if d.passwd == text_), None)  ##index de usuario
                if inde != None and validation_ and not self.isupdate and self.ownUsers[1][inde].user == self.noti_gest.trasfer_list[ind_].receiver:
                    (bo, f_date) = self.noti_gest.validarObservar(cod, datetime.now().strftime("%Y-%m-%d"))
                    if not bo and f_date != None:
                        index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
                        self.noti_gest.trasfer_list[index_].f_date = str(f_date)
                        self.noti_gest.trasfer_list[index_].state = "OBSERVADO"
                        ret = QMessageBox.question(self, 'Alerta', "La operación ya fue observada", QMessageBox.Ok, QMessageBox.Ok)
                    elif bo and f_date != None:
                        index_ = next((index for (index, d) in enumerate(self.noti_gest.trasfer_list) if d.cod == cod), None)
                        self.noti_gest.trasfer_list[index_].f_date = str(f_date)
                        self.noti_gest.trasfer_list[index_].state = "OBSERVADO"
                        ret = QMessageBox.question(self, 'Alerta', "Operación observada!!", QMessageBox.Ok, QMessageBox.Ok)
                elif inde != None and validation_ and not self.isupdate and self.ownUsers[1][inde].user != self.noti_gest.trasfer_list[ind_].receiver:
                    ret = QMessageBox.question(self, 'Alerta', "Debe observar el usuario que esta atendiendo", QMessageBox.Ok, QMessageBox.Ok)

        if not self.isupdate:
            self.fill_notificationtable()
            self.load_notifications()

    def fill_notificationtable(self):
        self.notificaciones.clear()
        for j in self.noti_gest.trasfer_list:
            data = {"cod": "TR" + str(j.cod),
                    "operacion": "TRASLADO",
                    "s_point": j.s_point,
                    "f_point": j.f_point,
                    "emiter": j.emiter,
                    "receiver": j.receiver,
                    "detalles": self.noti_gest.getText(j.items),
                    "s_date": j.s_date,
                    "f_date": j.f_date,
                    "estado": j.state,
                    "colors": j.colors}
            self.notificaciones.append(data)

    def init_conditions(self):
        self.noti_gest.getTransfers(self.ownWares[0])
        self.fill_notificationtable()
        self.load_notifications()

    def load_notifications(self, type = ""):
        #flag = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled
        row = 0
        self.notification_table.setRowCount(len(self.notificaciones))
        for ware_li in self.notificaciones:
            item = QtWidgets.QTableWidgetItem(ware_li["cod"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(ware_li["operacion"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 1, item)
            txt = "[" + ware_li["s_point"] + "]-->[" + ware_li["f_point"] + "]"
            self.notification_table.item(row, 1).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(str.upper(ware_li["receiver"]))
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 2, item)
            txt = "I:" + str.upper(ware_li["emiter"]) + "\nD:" + str.upper(ware_li["receiver"])
            self.notification_table.item(row, 2).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(ware_li["detalles"].replace('\n', ""))
            #item.setFlags(flag)
            self.notification_table.setItem(row, 3, item)
            self.notification_table.item(row, 3).setToolTip(ware_li["detalles"])

            item = QtWidgets.QTableWidgetItem(str(ware_li["f_date"]))
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 4, item)
            txt = "I:" + ware_li["s_date"] + "\nD:" + ware_li["f_date"]
            self.notification_table.item(row, 4).setToolTip(txt)

            item = QtWidgets.QTableWidgetItem(ware_li["estado"])
            #item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            self.notification_table.setItem(row, 5, item)
            if ware_li["estado"] == "ATENDIDO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["amarillo"][0], ware_li["colors"]["amarillo"][1],
                                 ware_li["colors"]["amarillo"][2]))

            elif ware_li["estado"] == "CERRADO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["verde"][0], ware_li["colors"]["verde"][1],
                                 ware_li["colors"]["verde"][2]))

            elif ware_li["estado"] == "OBSERVADO":
                self.notification_table.item(row, 5).setBackground(
                    QtGui.QColor(ware_li["colors"]["rojo"][0], ware_li["colors"]["rojo"][1],
                                 ware_li["colors"]["rojo"][2]))
            row += 1

    def open_wareWindow(self, event):
        self.ui_dialog.isupdateWare = self.isupdateWare
        self.ui_dialog.init_condition()
        # self.setEnabled(False)
        self.notification_table.clearSelection()
        self.isopenware = True
        #self.ui_dialog.show_window()
        if self.ui_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # self.setEnabled(True)
            self.isopenware = False
            self.isupdateWare = False

    def open_salesWindow(self):
        if self.sales_dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass


    def setupUi(self):
        width, height = pyautogui.size()
        self.w = width - 200
        self.h = height - 200
        #print("ancho: " + str(width) + " y altura: " + str(height))
        self.setObjectName("MainWindow")
        self.resize(self.w, self.h)
        self.setFixedSize(self.w, self.h)

        #self.qInput = QtWidgets.QInputDialog(self)
        # text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña", QtWidgets.QLineEdit.Password)
        #self.qInput.setInputMode(QtWidgets.QLineEdit.Password)

        # -----------  MenuBar Configuration  -----------
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.w, 20))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.Ingresos = QtWidgets.QMenu(self.menu)
        self.Ingresos.setObjectName("Ingresos")
        self.Salidas = QtWidgets.QMenu(self.menu)
        self.Salidas.setObjectName("Salidas")
        self.Reportes = QtWidgets.QMenu(self.menu)
        self.Reportes.setObjectName("Reportes")
        self.setMenuBar(self.menubar)

        self.Compras = QtWidgets.QAction(self)
        self.Compras.setObjectName("Compras")
        self.VentasD = QtWidgets.QAction(self)
        self.VentasD.setObjectName("VentasD")
        self.ConsignacionR = QtWidgets.QAction(self)
        self.ConsignacionR.setObjectName("ConsignacionR")
        self.VentasR = QtWidgets.QAction(self)
        self.VentasR.setObjectName("VentasR")
        self.ClientesR = QtWidgets.QAction(self)
        self.ClientesR.setObjectName("ClientesR")
        self.ProveedoresR = QtWidgets.QAction(self)
        self.ProveedoresR.setObjectName("ProveedoresR")
        self.Ingresos.addAction(self.Compras)
        self.Salidas.addAction(self.VentasD)
        self.Reportes.addAction(self.ConsignacionR)
        self.Reportes.addAction(self.VentasR)
        self.Reportes.addAction(self.ClientesR)
        self.Reportes.addAction(self.ProveedoresR)

        self.menu.addAction(self.Salidas.menuAction())
        self.menu.addAction(self.Ingresos.menuAction())
        self.menu.addAction(self.Reportes.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        # -----------  Triggered para QAction -----------
        self.VentasD.triggered.connect(self.open_salesWindow)

        # -----------  top frame configuration  -----------
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 20, self.w, 100))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # -----------  user label configuration  -----------
        self.user_label = QtWidgets.QLabel(self.frame)
        self.user_label.setGeometry(QtCore.QRect(self.w-220, 20, 191, 31))
        self.user_label.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.user_label.setObjectName("user_label")

        # -----------  ware label configuration  -----------
        self.ware_labe = QtWidgets.QLabel(self.frame)
        self.ware_labe.setGeometry(QtCore.QRect(self.w-500, 60, 255, 31))
        self.ware_labe.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.ware_labe.setObjectName("ware_labe")

        # -----------  date label configuration  -----------
        self.date_label = QtWidgets.QLabel(self.frame)
        self.date_label.setGeometry(QtCore.QRect(self.w-220, 60, 191, 31))
        self.date_label.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.date_label.setObjectName("date_label")
        self.brush_windows()

        # -----------  warelabel cofiguration  -----------
        self.ware_label = QtWidgets.QLabel(self.frame)
        self.ware_label.setGeometry(QtCore.QRect(30, 15, 72, 72))
        self.ware_label.setText("")
        self.ware_label.setPixmap(QtGui.QPixmap("C:/Users/IROJAS/Desktop/Genesis/UI_STNG/imgs/warehouse_icon.png"))
        self.ware_label.setScaledContents(True)
        self.ware_label.setObjectName("ware_label")
        self.ware_label.mousePressEvent = self.open_wareWindow

        # -----------  ******* cofiguration  -----------
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 120, self.w, 20))
        self.frame_2.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        #
        # -----------  notification table configuration  -----------
        self.notification_table = QtWidgets.QTableWidget(self)
        self.notification_table.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers)
        self.notification_table.setGeometry(QtCore.QRect(0, 140, self.w, self.h - 140))
        self.notification_table.setObjectName("notification_table")
        self.notification_table.setColumnCount(6)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(0, item)
        self.notification_table.setColumnWidth(0, 80)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(1, item)
        self.notification_table.setColumnWidth(1, 120)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(2, item)
        self.notification_table.setColumnWidth(2, 120)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(3, item)
        self.notification_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(4, item)
        self.notification_table.setColumnWidth(4, 120)

        item = QtWidgets.QTableWidgetItem()
        self.notification_table.setHorizontalHeaderItem(5, item)
        self.notification_table.setColumnWidth(5, 120)

        self.notification_table.horizontalHeader().setEnabled(False)
        self.notification_table.setSelectionBehavior(1)
        self.notification_table.setSelectionMode(1)
        self.notification_table.verticalHeader().hide()
        self.notification_table.itemDoubleClicked.connect(self.doubleClickItem)

        # -----------  seteo datos por defecto en ventana  -----------
        self.retranslateUi()

        # -----------  inicia hilo de ventana -----------
        self.run_threads()

        # self.setCentralWidget(self) #no activar esto por que se freezzea la ventana
        # #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(self)

    def update_datetime(self):
        k = 0
        while(enable_datetime):
            self.date_label.setText(datetime.now().strftime("%H:%M %d/%m/%Y"))
            if k < 600:
                time.sleep(0.5)
                k += 1
            if k == 600:
                if not self.isopenware:
                    self.notification_table.setEnabled(False)
                self.isupdate = True
                self.noti_gest.getTransfers(self.ownWares[0])
                self.fill_notificationtable()
                self.load_notifications()
                self.notification_table.setEnabled(True)
                self.isupdate = False
                k = 0

    def run_threads(self):
        self.t1 = threading.Thread(target=self.update_datetime)
        self.t1.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Genesis - [Museo del Libro]"))
        self.user_label.setText(_translate("MainWindow", "USER: " + self.usr_text.upper()))
        self.date_label.setText(_translate("MainWindow", "18:39 20/04/2021"))
        self.menu.setTitle(_translate("MainWindow", "Operaciones"))
        self.Ingresos.setTitle(_translate("MainWindow", "Ingresos"))
        self.Salidas.setTitle(_translate("MainWindow", "Salidas"))
        self.Reportes.setTitle(_translate("MainWindow", "Reportes"))
        self.Compras.setText(_translate("MainWindow", "Compras"))
        self.VentasD.setText(_translate("MainWindow", "Ventas"))
        self.ConsignacionR.setText(_translate("MainWindow", "Compras"))
        self.VentasR.setText(_translate("MainWindow", "Ventas"))
        self.ClientesR.setText(_translate("MainWindow", "Clientes"))
        self.ProveedoresR.setText(_translate("MainWindow","Proveedores"))
        self.ware_labe.setText(_translate("MainWindow", "ALMACEN: " + self.ware_name.upper()))
        self.ware_labe.adjustSize() #Ajusta el tamaño del label al tamaño de las letras
        self.ware_labe.move(self.w - 240 - self.ware_labe.width(), 66) #cambia la posicion del label

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setWeight(85)
        font.setBold(True)

        item = self.notification_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "código"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))

        item = self.notification_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "operación"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))

        item = self.notification_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "responsable"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))

        item = self.notification_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "detalles"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))


        item = self.notification_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "fecha"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))

        item = self.notification_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "estado"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0, 0, 0)))

        # font = QtGui.QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(8)
        # font.setWeight(75)
        # font.setBold(False)
        # self.notification_table.setRowCount(1)
        # flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        # item = QtWidgets.QTableWidgetItem("TR1")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter)
        # item.setFont(font)
        # self.notification_table.setItem(0, 0, item)
        #
        # item = QtWidgets.QTableWidgetItem("TRASLADO")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter)
        # item.setFont(font)
        # self.notification_table.setItem(0, 1, item)
        #
        # item = QtWidgets.QTableWidgetItem("")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter)
        # item.setFont(font)
        # self.notification_table.setItem(0, 2, item)
        #
        # item = QtWidgets.QTableWidgetItem("POR FAVOR, TRAER LOS LIBROS DE LA CASA CON LOS SIGUIENTES CODIGOS Y LUEGO LLEVAR A OTRO LUGAR CON")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter | Qt.AlignLeft)
        # item.setFont(font)
        # self.notification_table.setItem(0, 3, item)
        #
        # item = QtWidgets.QTableWidgetItem("")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter)
        # self.notification_table.setItem(0, 4, item)
        #
        # item = QtWidgets.QTableWidgetItem("ABIERTO")
        # item.setFlags(flag)
        # item.setTextAlignment(Qt.AlignCenter)
        # self.notification_table.setItem(0, 5, item)

    def brush_windows(self):
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
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ware_labe.setPalette(palette)
        self.user_label.setPalette(palette)
        self.date_label.setPalette(palette)
        self.ware_labe.setFont(font)
        self.user_label.setFont(font)
        self.date_label.setFont(font)

    def showDialog(self, details = "IVAN ROJAS CARRASCO"):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Question)
        self.msgBox.setText("Desea validar la operacion??, Presione Yes\n\n"
                            "Presione Abort en caso desee observar la operación")
        self.msgBox.setWindowTitle("Validación")
        self.msgBox.setDetailedText(details)
        self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort)
        self.msgBox.setEscapeButton(QMessageBox.No)
        #self.msgBox.buttonClicked.connect(self.msgButtonClick)
        return self.msgBox.exec()

    # def msgButtonClick(self, i):
    #     pass



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

