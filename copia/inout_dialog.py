# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inout_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import *
from gestor import ware_gestor
import time
import copy



class Ui_inoutDialog(QtWidgets.QDialog):
    def __init__(self, data_users = None, data_wares = None, parent=None):
        super(Ui_inoutDialog, self).__init__(parent)
        self.ownUsers = data_users
        self.ownWares = data_wares
        self.mainList = []
        self.duobleClickFlag = False
        self.main_table = []
        self.cantItems = 0
        self.valCell = ""
        self.operacion = None #define estado neutro para el closeevent
        self.ware_in = ware_gestor() #esto es para realizar el update
        self.setupUi()
        self.init_condition()

    #def show_window(self):
        #self.thread_.myValue = True
        #self.startProgressBar()
        #self.main_table.clear()
        #self.update_table()
        #self.cmbCriterio.setCurrentIndex(-1)
        #self.show()

    def init_condition(self):
        # -----------  set item conditions  -----------
        self.main_table.clear()
        self.cantItems = 0
        self.generalFlag = False
        item_all = ['cod','isbn','nombre','autor']
        items_operacion = ['ingreso', 'salida']
        self.cmbBusqueda.clear()
        self.cmbOperacion.clear()
        self.cmbBusqueda.addItems(item_all)
        self.in_tableWidget.clearContents()
        self.in_tableWidget.setRowCount(0)
        self.lblTitle_cant.setText("Items: 0")
        self.cmbOperacion.addItems(items_operacion)
        self.cmbBusqueda.setCurrentIndex(-1)
        self.cmbOperacion.setCurrentIndex(-1)
        self.txtBusqueda.clear()
        self.searchList.clear()

    def add_item(self, cod = ""):
        #main_table es lista para manejar los datos qtablewidget
        #index_ igual a None si no ecuentra coincidcnias
        index_ = next((index for (index, d) in enumerate(self.mainList) if d.objBook.cod == cod), None)
        flag = False
        if len(self.main_table) == 0:
            #_tmpObject = copy.copy(object_)
            data = {"cod": self.mainList[index_].objBook.cod, "isbn": self.mainList[index_].objBook.isbn, "name": self.mainList[index_].objBook.name, "cantidad": 1}
            self.main_table.append(data)
            self.updateTotalItems()
        else:
            #_tmpObject = copy.copy(object_)
            #data = {"cod": _tmpObject.book.cod, "isbn": _tmpObject.book.isbn, "name": _tmpObject.book.name, "cantidad": _tmpObject.almacen_quantity[0]}
            for item in self.main_table:
                if item["cod"] == cod:
                    flag = True
                    item["cantidad"] += 1 
            if flag == False:
                data = {"cod": self.mainList[index_].objBook.cod, "isbn": self.mainList[index_].objBook.isbn, "name": self.mainList[index_].objBook.name, "cantidad": 1}
                self.main_table.append(data)
        self.updateTotalItems()
        self.update_table()

    def update_table(self):
        flag = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled
        flag1 = QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable
        
        # -----------  esta parte para llenar la tabla  -----------
        row = 0
        self.in_tableWidget.setRowCount(len(self.main_table))

        for ware_li in self.main_table:
            item = QtWidgets.QTableWidgetItem(ware_li["cod"])
            item.setFlags(flag)
            self.in_tableWidget.setItem(row, 0, item)
            item = QtWidgets.QTableWidgetItem(ware_li["isbn"])
            item.setFlags(flag)
            self.in_tableWidget.setItem(row, 1, item)
            item = QtWidgets.QTableWidgetItem(ware_li["name"])
            item.setFlags(flag)
            self.in_tableWidget.setItem(row, 2, item)
            item = QtWidgets.QTableWidgetItem(str(ware_li["cantidad"]))
            item.setFlags(flag1)
            self.in_tableWidget.setItem(row, 3, item)
            row += 1

    def txtbusquedaAcept(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() == "isbn":
            if self.searchList.count() == 1:
                self.add_item(self.searchList.item(0).text().split(" ")[0].strip())
                self.txtBusqueda.clear()
            elif self.searchList.count() > 1:
                self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())

        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() != "isbn" and self.cmbBusqueda.currentIndex() != -1:
            if self.searchList.count() > 0:
                self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())

        return QtWidgets.QLineEdit.keyPressEvent(self.txtBusqueda, event)

    def listSearchKey(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() == "isbn":
            if self.searchList.count() == 1:
                self.add_item(self.searchList.item(0).text().split(" ")[0].strip())
                self.txtBusqueda.clear()
            elif self.searchList.count() > 1:
                self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())

        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() != "isbn" and self.cmbBusqueda.currentIndex() != -1:
            if self.searchList.count() > 0:
                self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())
        return QtWidgets.QListWidget.keyPressEvent(self.searchList, event)

    def txtBusquedaChanged(self):

        tmp_len = 0

        if self.cmbBusqueda.currentText() == "cod" and self.txtBusqueda.text() != "":
            self.searchList.clear()
            tmp_len = self.buscar("cod", self.txtBusqueda.text())

        elif self.cmbBusqueda.currentText() == "isbn" and self.txtBusqueda.text() != "":
            self.searchList.clear()
            tmp_len = self.buscar("isbn", self.txtBusqueda.text())

        elif self.cmbBusqueda.currentText() == "nombre" and self.txtBusqueda.text() != "":
            self.searchList.clear()
            tmp_len = self.buscar("nombre", self.txtBusqueda.text())

        elif self.cmbBusqueda.currentText() == "autor" and self.txtBusqueda.text() != "":
            self.searchList.clear()
            tmp_len = self.buscar("autor", self.txtBusqueda.text())

        elif self.txtBusqueda.text() == "":
            self.searchList.clear()

        if tmp_len == 0:
            self.searchList.clear()
        elif tmp_len > 0:
            self.searchList.setCurrentRow(0)

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(Ui_inoutDialog, self).keyPressEvent(event)

    def KeyPressed(self,event):
        if self.in_tableWidget.selectedIndexes() != []:
            if event.key() == QtCore.Qt.Key_Delete:
                temp = self.in_tableWidget.currentRow()
                self.main_table.pop(temp)
                self.updateTotalItems()
                self.update_table()
        return QtWidgets.QTableWidget.keyPressEvent(self.in_tableWidget, event)

    def onCmbIndexChanged(self):
        self.txtBusqueda.setText("")

    def buscar(self, criterio, patron):

        if criterio == "cod":
            k = 0
            for i in self.mainList:
                if i.objBook.cod == str.upper(patron):
                    if len(i.objBook.isbn) > 0:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " + 
                                                   i.objBook.name[:27] + " | " + i.objBook.autor[:15] + " | " + i.objBook.editorial[:8])
                        k += 1
                    else:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:28] + " | " + i.objBook.autor[:12] + " | " + i.objBook.editorial[:12])
                        k += 1
        elif criterio == "isbn":
            k = 0
            for i in self.mainList:
                if i.objBook.isbn.find(str.upper(patron)) >= 0:
                    if len(i.objBook.isbn) > 0:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:27] + " | " + i.objBook.autor[:15] + " | " + i.objBook.editorial[:8])
                        k += 1
                    else:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:28] + " | " + i.objBook.autor[:12] + " | " + i.objBook.editorial[:12])
                        k += 1
        elif criterio == "nombre":
            k = 0
            for i in self.mainList:
                if i.objBook.name.find(str.upper(patron)) >= 0:
                    if len(i.objBook.isbn) > 0:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:27] + " | " + i.objBook.autor[:15] + " | " + i.objBook.editorial[:8])
                        k += 1
                    else:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:28] + " | " + i.objBook.autor[:12] + " | " + i.objBook.editorial[:12])
                        k += 1

        elif criterio == "autor":
            k = 0
            for i in self.mainList:
                if i.objBook.autor.find(str.upper(patron)) >= 0:
                    if len(i.objBook.isbn) > 0:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:27] + " | " + i.objBook.autor[:15] + " | " + i.objBook.editorial[:8])
                        k += 1
                    else:
                        self.searchList.insertItem(k, i.objBook.cod + " | " + i.objBook.isbn + " | " +
                                                   i.objBook.name[:28] + " | " + i.objBook.autor[:12] + " | " + i.objBook.editorial[:12])
                        k += 1
        return k

    def changeIcon(self, item):

        if self.duobleClickFlag == True:
            row = item.row()
            col = item.column()
            try:
                cellValue = int(self.in_tableWidget.item(row,col).text())
                if cellValue > 0:
                    self.main_table[row]["cantidad"] = cellValue
                else:
                    self.in_tableWidget.item(row, 3).setText(self.valCell)
            except:
                ret = QMessageBox.information(self, 'Aviso', "Debe ingresar un numero entero")
                self.in_tableWidget.item(row,3).setText(self.valCell)

            self.updateTotalItems()
            self.duobleClickFlag = False

    def doubleClickItem(self, item):
        if item.column() == 3:
            self.duobleClickFlag = True
            self.valCell = self.in_tableWidget.item(item.row(), item.column()).text()

    def updateTotalItems(self):
        for i in self.main_table:
            self.cantItems += i["cantidad"]
        if self.in_tableWidget.rowCount() < 1:
            self.cantItems == 0
        self.lblTitle_cant.setText("Items: " + str(self.cantItems))
        self.cantItems = 0

    def aceptarEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.cmbOperacion.currentIndex() != -1:
                self.operacion = "aceptar"
                self.close()
            else:
                ret = QMessageBox.information(self, 'Aviso', "Debe ingresar criterio de operación")

    def closeEvent(self, event):
        if self.operacion == "aceptar":
            event.ignore()
            if self.in_tableWidget.rowCount() > 0:
                reply = QMessageBox.question(self, 'Window Close', 'Esta seguro de efectuar los cambios?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    if self.ware_in.update_quantity(self.main_table, self.cmbOperacion.currentText(), self.ownWares[0]):
                        self.generalFlag = True
                        self.accept()
                        event.accept()
                    else:
                        ret = QMessageBox.information(self, 'Aviso', "No se pudo conectar con la base de datos")
                        event.ignore()
                else:
                    event.ignore()
            else:
                ret = QMessageBox.information(self, 'Aviso', "No hay items agregados en tabla")
                event.ignore()
            self.operacion = None
        else:
            reply = QMessageBox.question(self, 'Window Close', 'al cerrar la ventana, se borraran los datos de la tabla', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.in_tableWidget.clearContents()
                self.in_tableWidget.setRowCount(0)
                self.generalFlag = False
                self.accept()
                event.accept()
            else:
                event.ignore()

    @property
    def return_val(self):
        return (self.main_table, self.cmbOperacion.currentText(), self.generalFlag)

    def setupUi(self):
        self.setObjectName("inoutDialog")
        self.resize(640, 360)
        self.setFixedSize(640,360)

        # -----------  top frame configuration  -----------
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 640, 65)) #width 640, height 65
        self.frame_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(22, 136, 126, 255), stop:1 rgba(56, 110, 142, 255));")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # -----------  groupBox configuration  -----------
        self.gbCriterio = QtWidgets.QGroupBox(self.frame_2)
        self.gbCriterio.setGeometry(QtCore.QRect(20, 0, 390, 60))
        #self.change_color_criterio() #funcion que cambia color y fuente de gbCriterio
        self.gbCriterio.setObjectName("gbCriterio")

        # -----------  QComboBox configuration  -----------
        self.cmbBusqueda = QtWidgets.QComboBox(self.gbCriterio)
        self.cmbBusqueda.setGeometry(QtCore.QRect(10, 23, 80, 30))
        self.cmbBusqueda.setStyleSheet("background-color: rgb(170, 255, 0);")
        font = QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cmbBusqueda.setFont(font)
        self.cmbBusqueda.setObjectName("cmbBusqueda")
        self.cmbBusqueda.currentIndexChanged.connect(self.onCmbIndexChanged)

        # -----------  QlineWidget configuration  -----------
        self.txtBusqueda = QtWidgets.QLineEdit(self.gbCriterio)
        self.txtBusqueda.setGeometry(QtCore.QRect(100, 23, 280, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.txtBusqueda.setFont(font)
        self.txtBusqueda.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.txtBusqueda.setClearButtonEnabled(True)
        self.txtBusqueda.setObjectName("txtBusqueda")
        #self.txtBusqueda.keyPressEvent = self.keyPressed_
        #self.txtBusqueda.mousePressEvent = self.holaMundo
        self.txtBusqueda.textChanged.connect(self.txtBusquedaChanged)
        self.txtBusqueda.keyPressEvent = self.txtbusquedaAcept

        # -----------  btnBuscar configuration  -----------
        #self.btnBuscar = QtWidgets.QPushButton(self.gbCriterio)
        #self.btnBuscar.setGeometry(QtCore.QRect(390, 23, 71, 30))
        #font = QtGui.QFont()
        #font.setFamily("Open Sans Semibold")
        #font.setPointSize(10)
        #font.setBold(True)
        #font.setWeight(75)
        #self.btnBuscar.setFont(font)
        #self.btnBuscar.setStyleSheet("background-color: rgb(240, 240, 240);")
        #self.btnBuscar.setObjectName("btnBuscar")
        #self.btnBuscar.clicked.connect(self.btnBuscarEvent)

        #self.btnBuscar.clicked.connect(self.btnBuscarEvent)

        #self.cmbCriterio = QtWidgets.QComboBox(self.gbCriterio)
        #self.cmbCriterio.setGeometry(QtCore.QRect(20, 23, 141, 30))
        #self.cmbCriterio.setStyleSheet("background-color: rgb(170, 255, 0);")
        #font = QFont()
        #font.setFamily("Open Sans Semibold")
        #font.setPointSize(10)
        #font.setBold(True)
        #font.setWeight(75)
        #self.cmbCriterio.setFont(font)
        #self.cmbCriterio.setObjectName("cmbCriterio")

        # -----------  qlist configuration  -----------
        self.searchList = QtWidgets.QListWidget(self)
        self.searchList.setGeometry(QtCore.QRect(0, 65, 640, 65))
        font = QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(45)
        self.searchList.setFont(font)
        self.searchList.setObjectName("searchList")
        self.searchList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchList.keyPressEvent = self.listSearchKey
        # -----------  mid-frame configuration  -----------
        self.mid_frame = QtWidgets.QFrame(self)
        self.mid_frame.setGeometry(QtCore.QRect(0, 130, 640, 5)) #width 640, height 65
        self.mid_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(22, 136, 126, 255), stop:1 rgba(56, 110, 142, 255));")
        self.mid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mid_frame.setObjectName("mid_frame")


        # -----------  in_tableWidget  -----------
        self.in_tableWidget = QtWidgets.QTableWidget(self)
        self.in_tableWidget.setGeometry(QtCore.QRect(0, 135, 640, 175))
        self.in_tableWidget.setObjectName("in_tableWidget")
        self.in_tableWidget.setColumnCount(4)
        self.in_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.in_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.in_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.in_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.in_tableWidget.setHorizontalHeaderItem(3, item)

        self.in_tableWidget.setColumnWidth(0,80)
        self.in_tableWidget.setColumnWidth(1,120)
        self.in_tableWidget.setColumnWidth(2,365)
        self.in_tableWidget.setColumnWidth(3,75)
        self.in_tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.in_tableWidget.horizontalHeader().setEnabled(False)
        self.in_tableWidget.setSelectionMode(1)
        self.in_tableWidget.setSelectionBehavior(1)
        self.in_tableWidget.setStyleSheet("selection-background-color: rgb(0, 120, 255);selection-color: rgb(255, 255, 255);")
        self.in_tableWidget.verticalHeader().hide()
        self.in_tableWidget.keyPressEvent = self.KeyPressed
        self.in_tableWidget.itemChanged.connect(self.changeIcon)
        self.in_tableWidget.itemDoubleClicked.connect(self.doubleClickItem)

        # -----------  bottom frame configuration  -----------
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 310, 640, 50))
        self.frame.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(22, 136, 126, 255), stop:1 rgba(56, 110, 142, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # -----------  lblCantidad Configuration  -----------
        self.lblTitle_cant = QtWidgets.QLabel(self.frame)
        self.lblTitle_cant.setGeometry(QtCore.QRect(520, 12, 391, 31))
        self.change_color_lbltitle()
        self.lblTitle_cant.setWordWrap(False)
        self.lblTitle_cant.setObjectName("lblTitle_cant")

        # -----------  groupBoxBottom configuration  -----------
        self.gbBottom = QtWidgets.QGroupBox(self.frame)
        self.gbBottom.setGeometry(QtCore.QRect(5, 5, 225, 40))
        self.change_color_criterio() #funcion que cambia color y fuente de gbCriterio
        self.gbBottom.setObjectName("gbBottom")


        # -----------  btn aceptar configutarion  -----------
        self.btnAceptar = QtWidgets.QPushButton(self.gbBottom)
        self.btnAceptar.setGeometry(QtCore.QRect(5, 5, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnAceptar.setFont(font)
        self.btnAceptar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnAceptar.setObjectName("btnAceptar")
        self.btnAceptar.setAutoExclusive(True)
        self.btnAceptar.mousePressEvent = self.aceptarEvent

        # -----------  QComboBox configuration  -----------
        self.cmbOperacion = QtWidgets.QComboBox(self.gbBottom)
        self.cmbOperacion.setGeometry(QtCore.QRect(115, 5, 100, 30))
        self.cmbOperacion.setStyleSheet("background-color: rgb(170, 255, 0);")
        font = QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cmbOperacion.setFont(font)
        self.cmbOperacion.setObjectName("cmbOperacion")
        #self.cmbOperacion.currentIndexChanged.connect(self.onCmbIndexChanged)


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbCriterio.setTitle(_translate("inoutDialog", "Cuadro de busqueda"))
        self.btnAceptar.setText(_translate("inoutDialog", "Aceptar"))
        #self.btnCancelar.setText(_translate("inoutDialog", "Cancelar"))
        self.lblTitle_cant.setText(_translate("inoutDialog", "Items: 0"))
        #self.btnBuscar.setText(_translate("Dialog", "Buscar"))
        
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setWeight(85)
        font.setBold(True)

        item = self.in_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("inoutDialog", "cod"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.in_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("inoutDialog", "isbn"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.in_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("inoutDialog", "nombre"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.in_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("inoutDialog", "cant."))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))

    def change_color_lbltitle(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblTitle_cant.setPalette(palette)
        self.lblTitle_cant.setFont(font)

    def change_color_criterio(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 1.0, 0.0, 0.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.298507, QtGui.QColor(22, 136, 126))
        gradient.setColorAt(1.0, QtGui.QColor(56, 110, 142))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.gbCriterio.setPalette(palette)
        self.gbCriterio.setFont(font)
        self.gbBottom.setPalette(palette)
        self.gbBottom.setFont(font)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_inoutDialog(Dialog)
    #ui.show_window()
    sys.exit(app.exec_())