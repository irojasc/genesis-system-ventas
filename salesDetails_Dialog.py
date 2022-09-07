import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QBrush, QColor, QStandardItem, QStandardItemModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from gestor import ware_gestor, customer_gestor

widgetHeight = 500
widgetWidth = 740


class sales_details(QtWidgets.QDialog):
    def __init__(self, widget, data_users = None, data_wares = None, parent=None):
        super(sales_details, self).__init__(parent)
        self.widget = widget
        self.ownUsers = data_users
        self.ownWares = data_wares
        self.ware = ware_gestor()
        self.custGest = customer_gestor()
        self.model = QStandardItemModel()

        # self.widget.currentChanged.connect(self.hola)
        self.setupUi()
        self.ware.load_items(self.ownWares[0])
        self.mainList = self.ware.ware_list.copy()
        self.main_table = []

    def init_condition(self):
        # -----------  set item conditions  -----------
        self.main_table.clear()
        self.cantCash = 0.0
        self.cantCredit = 0.0
        self.cantItems = 0
        # self.operacion = None
        # self.generalFlag = False
        # self.duobleClickFlag = False

        # -------- Se agrega los items para clientes --------#
        self.model.clear()
        for i in self.custGest.Customers:
            txt = i.doc + " | " + i.name
            self.model.appendRow(QStandardItem(txt))
        self.txtCliente.clear()
        self.main_table.clear()
        self.txtBusqueda.clear()
        self.searchList.clear()
        self.sales_tableWidget.clearContents()
        self.sales_tableWidget.setRowCount(0)
        self.lblTitle_cash.setText("Efectivo: S/.0.0")
        self.lblTitle_credit.setText("Tarjeta: S/.0.0")
        self.lblTitle_items.setText("Items: 0")

        # -------- Se agrea los items para cmb busqueda --------#
        item_all = ['cod', 'isbn', 'nombre', 'autor']
        self.cmbBusqueda.clear()
        self.cmbBusqueda.addItems(item_all)
        self.cmbBusqueda.setCurrentIndex(-1)

    # def hola(self, i):
    #     print(i)

    def updateTotalCashItems(self):
        self.cantItems = 0
        self.cantCash = 0.0
        self.cantCredit = 0.0
        if len(self.main_table) == 0:
            self.cantCash = 0.0
            # self.cantItems == 0
        elif len(self.main_table) > 0:
            for i in self.main_table:
                if i["tarjeta"]:
                    self.cantCredit += i["v.final"]
                else:
                    self.cantCash += i["v.final"]
                self.cantItems += i["cantidad"]

        self.lblTitle_items.setText("Items: " + str(self.cantItems))
        self.lblTitle_cash.setText("Efectivo: S/." + str(self.cantCash))
        self.lblTitle_credit.setText("Tarjeta: S/." + str(self.cantCredit))

    def SearclistKey(self, event):
        try:
            if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentIndex() != -1:
                if self.searchList.count() > 0:
                    self.add_item(self.searchList.item(self.searchList.currentRow()).text().split(" ")[0].strip())
        except:
            print("Falla en keyPressEvent de SearchList")
        return QtWidgets.QListWidget.keyPressEvent(self.searchList, event)

    def printcurrentwindow(self):
        print(self.widget.currentIndex())

    def update_table(self):
        self.loadFlag = True
        flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        flag1 = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

        # -----------  esta parte para llenar la tabla  -----------
        row = 0
        self.sales_tableWidget.setRowCount(len(self.main_table))
        for ware_li in self.main_table:
            # if self.ownWares[2][1] == True:
            #     self.in_tableWidget.item(row, 0).setToolTip(str(ware_li["ubic_" + self.ownWares[0]]))
            item = QtWidgets.QTableWidgetItem(ware_li["cod"])
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(ware_li["isbn"])
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["name"]))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 2, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["cantidad"]))
            item.setFlags(flag1)
            self.sales_tableWidget.setItem(row, 3, item)

            if ware_li["tarjeta"]:
                item = QtWidgets.QTableWidgetItem("VISA")
                item.setCheckState(Qt.Checked)
            elif not ware_li["tarjeta"]:
                item = QtWidgets.QTableWidgetItem("VISA")
                item.setCheckState(Qt.Unchecked)

            flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 4, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["serie"]))
            item.setFlags(flag1)
            self.sales_tableWidget.setItem(row, 5, item)

            # item = QtWidgets.QTableWidgetItem(str(ware_li["cliente"]))
            # item.setFlags(flag)
            # self.sales_tableWidget.setItem(row, 6, item)

            item = QtWidgets.QTableWidgetItem(str(ware_li["v.final"]))
            item.setFlags(flag1)
            self.sales_tableWidget.setItem(row, 6, item)

            row += 1
        self.loadFlag = False

    def changeIcon(self, item):
        row = item.row()
        column = item.column()
        if self.sales_tableWidget.item(row, 3) != None and not self.loadFlag and column == 3:
            try:
                cellValue = int(self.sales_tableWidget.item(row, 3).text())
                if cellValue > 0:
                    self.main_table[row]["cantidad"] = cellValue
                    self.main_table[row]["v.final"] = float(self.main_table[row]["cantidad"]) * self.main_table[row]["pv"]
                self.update_table()
            except:
                # ret = QMessageBox.information(self, 'Aviso', "Debe ingresar un numero entero")
                self.sales_tableWidget.item(row, 3).setText(str(self.main_table[row]["cantidad"]))

        elif self.sales_tableWidget.item(row, 6) != None and not self.loadFlag and column == 6:
            try:
                cellValue = float(self.sales_tableWidget.item(row, 6).text())
                if cellValue > 0:
                    self.main_table[row]["v.final"] = cellValue
                self.update_table()
            except:
                self.update_table()

        elif self.sales_tableWidget.item(row, 4) != None and not self.loadFlag and column == 4:
            if self.sales_tableWidget.item(row, 4).checkState() == QtCore.Qt.Checked:
                self.main_table[row]["tarjeta"] = True
            elif self.sales_tableWidget.item(row, 4).checkState() == QtCore.Qt.Unchecked:
                self.main_table[row]["tarjeta"] = False
            # try:
            #     cellValue = float(self.sales_tableWidget.item(row, 6).text())
            #     if cellValue > 0:
            #         self.main_table[row]["v.final"] = cellValue
            #     self.update_table()
            # except:
            #     self.update_table()
        self.updateTotalCashItems()

    def KeyPressed(self, event):
        list_rows = []
        if self.sales_tableWidget.selectedIndexes() != []:
            if event.key() == QtCore.Qt.Key_Delete:
                for item in self.sales_tableWidget.selectedIndexes():
                    list_rows.append(item.row())
                list_rows = list(dict.fromkeys(list_rows))
                list_rows.sort(reverse=True)
                for i in list_rows:
                    self.main_table.pop(i)
                self.update_table()
                self.updateTotalCashItems()
        return QtWidgets.QTableWidget.keyPressEvent(self.sales_tableWidget, event)

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
                    "serie": "pendiente",
                    "cliente": "",
                    "v.final": self.mainList[index_].objBook.Pv,
                    "pv": self.mainList[index_].objBook.Pv}
            self.main_table.append(data)
        else:
            for item in self.main_table:
                if item["cod"] == cod:
                    flag = True
                    item["cantidad"] += 1
                    item["v.final"] = float(item["cantidad"]) * item["pv"]
            if flag == False:
                data = {"id": 0,
                        "cod": self.mainList[index_].objBook.cod,
                        "isbn": self.mainList[index_].objBook.isbn,
                        "name": self.mainList[index_].objBook.name,
                        "cantidad": 1,
                        "tarjeta": False,
                        "serie": "pendiente",
                        "cliente": "",
                        "v.final": self.mainList[index_].objBook.Pv,
                        "pv": self.mainList[index_].objBook.Pv}
                self.main_table.append(data)
        self.update_table()
        if len(self.main_table) > 0:
            self.sales_tableWidget.setCurrentCell(0, 0)
        self.updateTotalCashItems()

    def txtbusquedaAcept(self, event):
        if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() == "isbn":
            if self.searchList.count() == 1:
                self.add_item(self.searchList.item(0).text().split(" ")[0].strip())
                self.txtBusqueda.clear()

        elif (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.cmbBusqueda.currentText() != "isbn" and self.cmbBusqueda.currentIndex() != -1:
            if self.searchList.count() > 0:
                self.add_item(self.searchList.item(0).text().split(" ")[0].strip())

        return QtWidgets.QLineEdit.keyPressEvent(self.txtBusqueda, event)

    def onCmbIndexChanged(self):
        self.txtBusqueda.clear()

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
            super(sales_details, self).keyPressEvent(event)

    def regresarButtonEvent(self, event):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

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
        self.gbCriterio.setGeometry(QtCore.QRect(10, 0, 390, 60))
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


        # -----------  groupBox configuration  -----------
        self.gbCustomer = QtWidgets.QGroupBox(self.frame_2)
        self.gbCustomer.setGeometry(QtCore.QRect(410, 0, 250, 60))
        self.gbCustomer.setObjectName("gbCustomer")

        # -----------  QlineCustomer configuration  -----------
        self.txtCliente = QtWidgets.QLineEdit(self.gbCustomer)
        self.txtCliente.setGeometry(QtCore.QRect(10, 23, 230, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(55)
        self.txtCliente.setFont(font)
        self.txtCliente.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtCliente.setClearButtonEnabled(True)
        self.txtCliente.setObjectName("txtCliente")
        completer = QCompleter(self.model, self)
        self.txtCliente.setCompleter(completer)
        # self.txtCliente.textChanged.connect(self.txtBusquedaChanged) #ultimas variaciones
        # self.txtCliente.keyPressEvent = self.txtbusquedaAcept  #ultimas variaciones


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
        self.searchList.keyPressEvent = self.SearclistKey

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
        self.sales_tableWidget.setColumnCount(7)
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
        # item = QtWidgets.QTableWidgetItem()
        # self.sales_tableWidget.setHorizontalHeaderItem(7, item)

        self.sales_tableWidget.setColumnWidth(0, 65)
        self.sales_tableWidget.setColumnWidth(1, 95)
        self.sales_tableWidget.setColumnWidth(2, 310)
        self.sales_tableWidget.setColumnWidth(3, 40)
        self.sales_tableWidget.setColumnWidth(4, 65)
        self.sales_tableWidget.setColumnWidth(5, 70)
        self.sales_tableWidget.setColumnWidth(6, 110)
        # self.sales_tableWidget.setColumnWidth(7, 75)
        self.sales_tableWidget.horizontalHeader().setEnabled(False)
        self.sales_tableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.sales_tableWidget.setSelectionMode(1) #1 Single selection
        self.sales_tableWidget.setSelectionBehavior(1) #1 para selection de only rows
        self.sales_tableWidget.setStyleSheet("selection-background-color: rgb(0, 120, 255);selection-color: rgb(255, 255, 255);")
        self.sales_tableWidget.verticalHeader().hide()
        self.sales_tableWidget.keyPressEvent = self.KeyPressed
        self.sales_tableWidget.itemChanged.connect(self.changeIcon)
        # self.sales_tableWidget.itemChanged.connect(self.changeIcon)

        # -----------  bottom frame configuration  -----------
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, widgetHeight - 50, widgetWidth, 50))
        self.frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # -----------  lblCash Configuration  -----------
        self.lblTitle_cash = QtWidgets.QLabel(self.frame)
        self.lblTitle_cash.setGeometry(QtCore.QRect(607, 0, 360, 25))
        self.lblTitle_cash.setWordWrap(False)
        self.lblTitle_cash.setObjectName("lblTitle_cash")

        # -----------  lblCredit Configuration  -----------
        self.lblTitle_credit = QtWidgets.QLabel(self.frame)
        self.lblTitle_credit.setGeometry(QtCore.QRect(610, 25, 360, 25))
        self.lblTitle_credit.setWordWrap(False)
        self.lblTitle_credit.setObjectName("lblTitle_credit")

        # -----------  lblCredit Configuration  -----------
        self.lblTitle_items = QtWidgets.QLabel(self.frame)
        self.lblTitle_items.setGeometry(QtCore.QRect(475, 0, 100, 25))
        self.lblTitle_items.setWordWrap(False)
        self.lblTitle_items.setObjectName("lblTitle_items")

        # -----------  groupBoxBottom configuration  -----------
        self.gbBottom = QtWidgets.QGroupBox(self.frame)
        self.gbBottom.setGeometry(QtCore.QRect(5, 5, 220, 40))
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

        # -----------  btnregresar configutarion  -----------
        self.btnregresar = QtWidgets.QPushButton(self.gbBottom)
        self.btnregresar.setGeometry(QtCore.QRect(115, 5, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btnregresar.setFont(font)
        self.btnregresar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnregresar.setObjectName("btnGuardar")
        self.btnregresar.setAutoExclusive(True)
        self.btnregresar.mousePressEvent = self.regresarButtonEvent

        self.change_color_lbltitle()
        self.change_color_criterio()  # funcion que cambia color y fuente de gbCriterio
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.widget.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbCriterio.setTitle(_translate("Dialog", "Cuadro de busqueda"))
        self.gbCustomer.setTitle(_translate("Dialog", "Cliente"))
        self.btnGuardar.setText(_translate("Dialog", "Guardar"))
        self.btnregresar.setText(_translate("Dialog", "Regresar"))

        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setWeight(65)
        font.setBold(True)

        item = self.sales_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("salesDialog", "cod"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("salesDialog", "isbn"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("salesDialog", "titulo"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("salesDialog", "cant."))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("salesDialog", "tarjeta"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))
        item = self.sales_tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("salesDialog", "serie"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))

        # item = self.sales_tableWidget.horizontalHeaderItem(6)
        # item.setText(_translate("salesDialog", "cliente"))
        # item.setFont(font)
        # item.setForeground(QBrush(QColor(0,0,0)))

        item = self.sales_tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("salesDialog", "S/.(Valor)"))
        item.setFont(font)
        item.setForeground(QBrush(QColor(0,0,0)))

    def change_color_lbltitle(self):
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(65)
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
        self.lblTitle_cash.setFont(font)
        self.lblTitle_cash.setPalette(palette)
        self.lblTitle_items.setFont(font)
        self.lblTitle_items.setPalette(palette)

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 0))
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
        self.lblTitle_credit.setFont(font)
        self.lblTitle_credit.setPalette(palette)

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
        self.gbCustomer.setPalette(palette)
        self.gbCustomer.setFont(font)
        self.gbBottom.setPalette(palette)
        self.gbBottom.setFont(font)