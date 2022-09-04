import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from gestor import ware_gestor
from datetime import datetime, timedelta

today = datetime.now()
widgetHeight = 500
widgetWidth = 740

class sales_Dialog(QtWidgets.QDialog):
    def __init__(self, data_users = None, data_wares = None, parent=None):
        super(sales_Dialog, self).__init__(parent)
        self.ownUsers = data_users
        self.ownWares = data_wares
        self.ware = ware_gestor()
        self.widget = QtWidgets.QStackedWidget()
        self.dialog = QDialog()
        self.ui_dialog_ = customer_Dialog(self.widget, self.dialog)
        self.widget.addWidget(self)
        self.widget.addWidget(self.ui_dialog_)
        self.widget.setFixedHeight(widgetHeight)
        self.widget.setFixedWidth(widgetWidth)
        # self.widget.currentChanged.connect(self.hola)

        self.setupUi()
        self.ware.load_items(self.ownWares[0])
        self.mainList = self.ware.ware_list.copy()
        self.main_table = []

        self.cmbDateIndex = 0

        # item_all = ['22-09-2022']
        # self.cmbDate.clear()
        # self.cmbDate.addItems(item_all)
        # self.sales_tableWidget.setRowCount(1)
        # item = QtWidgets.QTableWidgetItem("99")
        # self.sales_tableWidget.setItem(0, 0, item)
        # item = QtWidgets.QTableWidgetItem("GN_9999")
        # self.sales_tableWidget.setItem(0, 1, item)
        # item = QtWidgets.QTableWidgetItem("9781741799965")
        # self.sales_tableWidget.setItem(0, 2, item)
        # item = QtWidgets.QTableWidgetItem("DOMINACION SIN DOMINIO EL ENCUENTRO INCA-ESPAÑOL"[:35])
        # self.sales_tableWidget.setItem(0, 3, item)
        # item = QtWidgets.QTableWidgetItem("99")
        # self.sales_tableWidget.setItem(0, 4, item)
        # flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        # # flag = QtCore.Qt.ItemIsEnabled
        # item = QtWidgets.QTableWidgetItem("VISA")
        # item.setCheckState(Qt.Unchecked)
        # item.setFlags(flag)
        # self.sales_tableWidget.setItem(0, 5, item)
        #
        # item = QtWidgets.QTableWidgetItem("B1-99999")
        # self.sales_tableWidget.setItem(0, 6, item)
        #
        # item = QtWidgets.QTableWidgetItem("GUILLERMO")
        # self.sales_tableWidget.setItem(0, 7, item)
        #
        # item = QtWidgets.QTableWidgetItem("9999.9")
        # self.sales_tableWidget.setItem(0, 8, item)

    def init_condition(self):
        # -----------  set item conditions  -----------

        self.main_table.clear()
        # self.cantItems = 0
        # self.operacion = None
        # self.generalFlag = False
        # self.duobleClickFlag = False

        # -------- Se agrea los items para los dos combos --------#
        yest = today - timedelta(1)
        befYest = today - timedelta(2)
        item_all = ['cod', 'isbn', 'nombre', 'autor']
        item_dates = [today.strftime("%d-%m-%Y"), yest.strftime("%d-%m-%Y"), befYest.strftime("%d-%m-%Y")]
        self.cmbBusqueda.clear()
        self.cmbBusqueda.addItems(item_all)
        self.cmbBusqueda.setCurrentIndex(-1)
        self.cmbDate.clear()
        self.cmbDate.addItems(item_dates)
        self.cmbDate.blockSignals(True)
        self.cmbDate.setCurrentIndex(0)
        self.cmbDate.blockSignals(False)
        # self.in_tableWidget.clearContents()
        # self.in_tableWidget.setRowCount(0)
        # self.lblTitle_cant.setText("Items: 0")
        self.txtBusqueda.clear()
        self.searchList.clear()

    def gotoScreen2(self):
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def hola(self, i):
        print(i)

    def printcurrentwindow(self):
        print(self.widget.currentIndex())

    def add_item(self, cod = ""):
        #main_table es lista para manejar los datos qtablewidget
        #index_ igual a None si no ecuentra coincidcnias
        index_ = next((index for (index, d) in enumerate(self.mainList) if d.objBook.cod == cod), None)
        flag = False
        if len(self.main_table) == 0:
            data = {"id": 0,
                    "cod": self.mainList[index_].objBook.cod,
                    "isbn": self.mainList[index_].objBook.isbn,
                    "name": self.mainList[index_].objBook.name,
                    "cantidad": 1,
                    "tarjeta": False,
                    "serie": "",
                    "cliente": "",
                    "v.final": self.mainList[index_].objBook.Pv}
            self.main_table.append(data)
            # self.updateTotalItems()
        # else:
        #     #_tmpObject = copy.copy(object_)
        #     #data = {"cod": _tmpObject.book.cod, "isbn": _tmpObject.book.isbn, "name": _tmpObject.book.name, "cantidad": _tmpObject.almacen_quantity[0]}
        #     for item in self.main_table:
        #         if item["cod"] == cod:
        #             flag = True
        #             item["cantidad"] += 1
        #     if flag == False:
        #         data = {"cod": self.mainList[index_].objBook.cod, "isbn": self.mainList[index_].objBook.isbn,
        #                 "name": self.mainList[index_].objBook.name, "cantidad": 1, "ubic_" + self.ownWares[0]: self.mainList[index_].almacen_data["ubic_" + self.ownWares[0]]}
        #         self.main_table.append(data)
        self.update_table()
        #
        if len(self.main_table) == 1:
            self.sales_tableWidget.setCurrentCell(0, 0)
        # self.updateTotalItems()

    def update_table(self):
        # self.loadFlag = True
        flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        flag1 = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

        # -----------  esta parte para llenar la tabla  -----------
        row = 0
        self.sales_tableWidget.setRowCount(len(self.main_table))
        for ware_li in self.main_table:

            item = QtWidgets.QTableWidgetItem(str(ware_li["id"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 0, item)
            # if self.ownWares[2][1] == True:
            #     self.in_tableWidget.item(row, 0).setToolTip(str(ware_li["ubic_" + self.ownWares[0]]))

            item = QtWidgets.QTableWidgetItem(ware_li["cod"])
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem(ware_li["isbn"])
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 2, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["name"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 3, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["cantidad"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 4, item)

            flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
            item = QtWidgets.QTableWidgetItem("VISA")
            item.setCheckState(Qt.Unchecked)
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 5, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["serie"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 6, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["cliente"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 7, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["v.final"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 8, item)

            row += 1
        # self.loadFlag = False

    def txtbusquedaAcept(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() == "isbn":
            if self.searchList.count() == 1:
                self.add_item(self.searchList.item(0).text().split(" ")[0].strip())
                self.txtBusqueda.clear()

        elif (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() != "isbn" and self.cmbBusqueda.currentIndex() != -1:
            pass
            # if self.searchList.count() > 0:
            #     self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())

        return QtWidgets.QLineEdit.keyPressEvent(self.txtBusqueda, event)

    def onCmbIndexChanged(self):
        self.txtBusqueda.clear()

    def onCmbDateIndexChanged(self, i):

        text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación',
                                                            "Ingrese contraseña para cambiar de fecha",
                                                            QtWidgets.QLineEdit.Password)
        index = next((index for (index, d) in enumerate(self.ownUsers[1]) if d == text_), None)
        # index = next((index for (index, d) in enumerate(self.ownUsers[1]) if d.passwd == text_), None)

        if index != None and validation_:
            print("Cambio hacia index: " + str(i))
            self.cmbDateIndex = i

        elif index == None and validation_:
            self.cmbDate.blockSignals(True)
            self.cmbDate.setCurrentIndex(self.cmbDateIndex)
            self.cmbDate.blockSignals(False)

        elif not validation_:
            self.cmbDate.blockSignals(True)
            self.cmbDate.setCurrentIndex(self.cmbDateIndex)
            self.cmbDate.blockSignals(False)

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

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(sales_Dialog, self).keyPressEvent(event)

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(widgetWidth, widgetHeight)
        self.setFixedSize(widgetWidth, widgetHeight)

        # -----------  top frame configuration  -----------
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, widgetWidth, 65)) #width 640, height 65
        self.frame_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # -----------  groupBox configuration  -----------
        self.gbCriterio = QtWidgets.QGroupBox(self.frame_2)
        self.gbCriterio.setGeometry(QtCore.QRect(20, 0, 390, 60))
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
        # self.txtBusqueda.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.txtBusqueda.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtBusqueda.setClearButtonEnabled(True)
        self.txtBusqueda.setObjectName("txtBusqueda")
        self.txtBusqueda.textChanged.connect(self.txtBusquedaChanged) #ultimas variaciones
        self.txtBusqueda.keyPressEvent = self.txtbusquedaAcept  #ultimas variaciones


        # -----------  groupBoxDate configuration  -----------
        self.gbDate = QtWidgets.QGroupBox(self.frame_2)
        self.gbDate.setGeometry(QtCore.QRect(420, 0, 128, 60))
        self.gbDate.setObjectName("gbDate")

        # -----------  QComboDate configuration  -----------
        self.cmbDate = QtWidgets.QComboBox(self.gbDate)
        self.cmbDate.blockSignals(True)
        self.cmbDate.setGeometry(QtCore.QRect(10, 23, 110, 30))
        self.cmbDate.setStyleSheet("background-color: rgb(170, 255, 0);")
        font = QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cmbDate.setFont(font)
        self.cmbDate.setObjectName("cmbDate")
        self.cmbDate.currentIndexChanged.connect(self.onCmbDateIndexChanged)

        # -----------  qlist configuration  -----------
        self.searchList = QtWidgets.QListWidget(self)
        self.searchList.setGeometry(QtCore.QRect(0, 65, widgetWidth, 65))
        font = QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(45)
        self.searchList.setFont(font)
        self.searchList.setObjectName("searchList")
        self.searchList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.searchList.keyPressEvent = self.listSearchKey

        # -----------  mid-frame configuration  -----------
        self.mid_frame = QtWidgets.QFrame(self)
        self.mid_frame.setGeometry(QtCore.QRect(0, 130, widgetWidth, 5)) #width 640, height 65
        self.mid_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.mid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mid_frame.setObjectName("mid_frame")

        # -----------  sales_tableWidget  -----------
        self.sales_tableWidget = QtWidgets.QTableWidget(self)
        self.sales_tableWidget.setGeometry(QtCore.QRect(0, 135, widgetWidth, widgetHeight - 185))
        self.sales_tableWidget.setObjectName("sales_tableWidget")
        self.sales_tableWidget.setColumnCount(9)
        self.sales_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.sales_tableWidget.setHorizontalHeaderItem(8, item)

        self.sales_tableWidget.setColumnWidth(0, 5)
        self.sales_tableWidget.setColumnWidth(1, 55)
        self.sales_tableWidget.setColumnWidth(2, 85)
        self.sales_tableWidget.setColumnWidth(3, 248)
        self.sales_tableWidget.setColumnWidth(4, 48)
        self.sales_tableWidget.setColumnWidth(5, 60)
        self.sales_tableWidget.setColumnWidth(6, 55)
        self.sales_tableWidget.setColumnWidth(7, 75)
        self.sales_tableWidget.setColumnWidth(8, 55)
        self.sales_tableWidget.horizontalHeader().setEnabled(False)
        self.sales_tableWidget.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        # self.sales_tableWidget.horizontalHeader().setEnabled(False)
        # self.sales_tableWidget.setSelectionMode(1)
        # self.sales_tableWidget.setSelectionBehavior(1)
        self.sales_tableWidget.setStyleSheet("selection-background-color: rgb(0, 120, 255);selection-color: rgb(255, 255, 255);")
        self.sales_tableWidget.verticalHeader().hide()
        # self.sales_tableWidget.keyPressEvent = self.KeyPressed
        # self.sales_tableWidget.itemChanged.connect(self.changeIcon)

        # -----------  bottom frame configuration  -----------
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, widgetHeight - 50, widgetWidth, 50))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # -----------  lblCantidad Configuration  -----------
        self.lblTitle_cant = QtWidgets.QLabel(self.frame)
        self.lblTitle_cant.setGeometry(QtCore.QRect(520, 12, 391, 31))
        self.lblTitle_cant.setWordWrap(False)
        self.lblTitle_cant.setObjectName("lblTitle_cant")

        # -----------  groupBoxBottom configuration  -----------
        self.gbBottom = QtWidgets.QGroupBox(self.frame)
        self.gbBottom.setGeometry(QtCore.QRect(5, 5, 110, 40))
        self.gbBottom.setObjectName("gbBottom")

        # -----------  btn Guardar configutarion  -----------
        self.btnGuardar = QtWidgets.QPushButton(self.gbBottom)
        self.btnGuardar.setGeometry(QtCore.QRect(5, 5, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnGuardar.setFont(font)
        self.btnGuardar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnGuardar.setObjectName("btnGuardar")
        self.btnGuardar.setAutoExclusive(True)
        # self.btnGuardar.mousePressEvent = self.aceptarEvent
        self.change_color_lbltitle()
        self.change_color_criterio()  # funcion que cambia color y fuente de gbCriterio
        self.retranslateUi()

    def loadItems(self):
        pass

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.widget.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbCriterio.setTitle(_translate("Dialog", "Cuadro de busqueda"))
        self.gbDate.setTitle(_translate("Dialog", "Fecha"))
        self.btnGuardar.setText(_translate("Dialog", "Guardar"))


        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setWeight(65)
        font.setBold(True)

        item = self.sales_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("salesDialog", "id"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("salesDialog", "cod"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("salesDialog", "isbn"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("salesDialog", "titulo"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("salesDialog", "cant."))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("salesDialog", "tarjeta"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("salesDialog", "serie"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("salesDialog", "cliente"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("salesDialog", "S/.(Valor)"))
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
        self.gbDate.setPalette(palette)
        self.gbDate.setFont(font)
        self.gbBottom.setPalette(palette)
        self.gbBottom.setFont(font)




















class customer_Dialog(QtWidgets.QDialog):
    # def __init__(self, data_users = None, data_wares = None, parent=None):
    def __init__(self, widget, parent=None):
        super(customer_Dialog, self).__init__(parent)
        self.widget = widget
        self.setupUi()
    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(widgetWidth, widgetHeight)
        self.setFixedSize(widgetWidth, widgetHeight)
        label = QLabel("Ivan Rojas 2", self)
        # setting geometry
        label.setGeometry(20, 20, 200, 60)
        self.Button = QtWidgets.QPushButton('Ir a ventana 1', self)
        self.Button.setGeometry(30, 200, 200, 25)
        self.Button.clicked.connect(self.gotoScreen1)
        self.retranslateUi()

    def gotoScreen1(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog_ = QDialog()
    ware_List = ["ALYZ", "SNTG", "STC"]
    users = ["hola mundo", ("catalina", "chuspa")]
    ui_dialog = sales_Dialog(users, ware_List, dialog_)
    ui_dialog.init_condition()
    ui_dialog.widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")
