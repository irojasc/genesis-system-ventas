import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from gestor import sales_gestor, customer_gestor
from salesDetails_Dialog import sales_details
from reniec_ import ApisNetPe
from datetime import datetime, timedelta

today = datetime.now()
widgetHeight = 500
widgetWidth = 740
API_TOKEN = "apis-token-2814.q18Q3i-X4yiph2RUT6IAkEZjb3efgrxa"


class sales_Dialog(QtWidgets.QDialog):
    # def __init__(self, data_users = None, data_wares = None, parent=None):
    def __init__(self, data_users = None, data_wares = None, parent = None):
        super(sales_Dialog, self).__init__(parent)
        self.ownUsers = data_users
        self.ownWares = data_wares
        self.widget = QtWidgets.QStackedWidget()
        self.dialog = QDialog()
        self.dialog_ = QDialog()
        self.ui_dialog_ = sales_details(self.widget, data_users, data_wares, self.dialog) #este es un Qdialog
        self.cust_dialog_ = customer_Dialog(self.widget, self.dialog_) #este es un Qdialog
        self.salesGest = sales_gestor(True)
        self.widget.addWidget(self)
        self.widget.addWidget(self.ui_dialog_)
        self.widget.addWidget(self.cust_dialog_)
        self.widget.setFixedHeight(widgetHeight)
        self.widget.setFixedWidth(widgetWidth)
        self.widget.currentChanged.connect(self.widgetChanged)
        self.setupUi()
        self.salesTable = []
        self.loadFlag = False

    def init_condition(self):
        self.ui_dialog_.loadItems()
        self.ui_dialog_.custGest.fill_customers()
        yest = today - timedelta(1)
        befYest = today - timedelta(2)
        item_dates = [today.strftime("%d-%m-%Y"), yest.strftime("%d-%m-%Y"), befYest.strftime("%d-%m-%Y")]
        self.cmbDate.blockSignals(True)
        self.cmbDate.clear()
        self.cmbDate.addItems(item_dates)
        self.cmbDate.setCurrentIndex(0)
        self.cmbDate.blockSignals(False)
        self.cmbDateIndex = 0
        self.loadTable()

    def updateTotalCashItems(self):
        self.cantCash = 0.0
        self.cantCredit = 0.0
        if len(self.salesTable) == 0:
            self.cantCash = 0.0
            self.cantCredit = 0.0
        elif len(self.salesTable) > 0:
            for i in self.salesTable:
                if i.credit:
                    self.cantCredit += i.total
                else:
                    self.cantCash += i.total
        # self.lblTitle_items.setText("Items: " + str(self.cantItems))
        self.lblTitle_cash.setText("Efectivo: S/." + str(self.cantCash))
        self.lblTitle_credit.setText("Tarjeta: S/." + str(self.cantCredit))

    def loadTable(self):
        date = self.cmbDate.currentText().split("-")[2] + "-" + self.cmbDate.currentText().split("-")[1] + "-" + self.cmbDate.currentText().split("-")[0]
        self.salesGest.loadSalesDetails(self.ownWares[0], date)
        self.loadtableWidget("main")

    def loadtableWidget(self, condition = "search"):
        self.loadFlag = True
        flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        flag1 = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

        if condition == "main":
            self.salesTable.clear()
            self.salesTable = self.salesGest.sales.copy()

        # -----------  esta parte para llenar la tabla  -----------
        row = 0
        self.sales_tableWidget.setRowCount(len(self.salesTable))
        for saleItem in self.salesTable:
            # if self.ownWares[2][1] == True:
            #     self.in_tableWidget.item(row, 0).setToolTip(str(ware_li["ubic_" + self.ownWares[0]]))
            item = QtWidgets.QTableWidgetItem(str(saleItem.id))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(saleItem.codbook)
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 1, item)

            item = QtWidgets.QTableWidgetItem(saleItem.isbn)
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 2, item)

            item = QtWidgets.QTableWidgetItem(saleItem.title)
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 3, item)

            item = QtWidgets.QTableWidgetItem(str(saleItem.cant))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 4, item)

            if saleItem.credit:
                item = QtWidgets.QTableWidgetItem("VISA")
                item.setCheckState(Qt.Checked)
            elif not saleItem.credit:
                item = QtWidgets.QTableWidgetItem("VISA")
                item.setCheckState(Qt.Unchecked)
            # flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 5, item)

            item = QtWidgets.QTableWidgetItem(saleItem.receipt)
            if not saleItem.block:
                item.setFlags(flag1) #flag1, editable
            elif saleItem.block:
                item.setFlags(flag) # not editable
            self.sales_tableWidget.setItem(row, 6, item)

            item = QtWidgets.QTableWidgetItem(saleItem.customer.split(" ")[0])
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 7, item)

            item = QtWidgets.QTableWidgetItem(str(saleItem.total))
            item.setFlags(flag)
            self.sales_tableWidget.setItem(row, 8, item)

            row += 1
        self.updateTotalCashItems()
        self.loadFlag = False

    def onCmbDateIndexChanged(self, i):

        text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación',
                                                            "Ingrese contraseña para cambiar de fecha",
                                                            QtWidgets.QLineEdit.Password)
        index = next((index for (index, d) in enumerate(self.ownUsers[1]) if d.passwd == text_), None)

        if index != None and validation_:
            date = self.cmbDate.currentText().split("-")[2] + "-" + self.cmbDate.currentText().split("-")[1] + "-" + \
                   self.cmbDate.currentText().split("-")[0]
            self.salesGest.loadSalesDetails(self.ownWares[0], date)
            self.cmbDateIndex = i
            self.loadtableWidget("main")

        elif index == None and validation_:
            self.cmbDate.blockSignals(True)
            self.cmbDate.setCurrentIndex(self.cmbDateIndex)
            self.cmbDate.blockSignals(False)

        elif not validation_:
            self.cmbDate.blockSignals(True)
            self.cmbDate.setCurrentIndex(self.cmbDateIndex)
            self.cmbDate.blockSignals(False)

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(sales_Dialog, self).keyPressEvent(event)

    def changeScreen(self, event):
        data = []
        for i in self.salesTable:
            if i.id == 0:
                data.append((i.id_, i.codbook, i.credit))
        date = self.cmbDate.currentText().split("-")[2] + "-" + self.cmbDate.currentText().split("-")[1] + "-" + \
               self.cmbDate.currentText().split("-")[0]
        self.ui_dialog_.DateSales = date
        self.ui_dialog_.init_condition()
        self.ui_dialog_.comparativeList = tuple(data)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(widgetWidth, widgetHeight)
        self.setFixedSize(widgetWidth, widgetHeight)

        # -----------  top frame configuration  -----------
        self.topFrame = QtWidgets.QFrame(self)
        self.topFrame.setGeometry(QtCore.QRect(0, 0, widgetWidth, 65)) #width 640, height 65
        self.topFrame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.topFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topFrame.setObjectName("topFrame")

        # -----------  groupBoxDate configuration  -----------
        self.gbDate = QtWidgets.QGroupBox(self.topFrame)
        self.gbDate.setGeometry(QtCore.QRect(15, 0, 128, 60))
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

        # -----------  File Icon cofiguration  -----------
        self.file_label = QtWidgets.QLabel(self.topFrame)
        self.file_label.setGeometry(QtCore.QRect(160, 9, 35, 49))
        self.file_label.setText("")
        self.file_label.setPixmap(QtGui.QPixmap("C:/Users/IROJAS/PycharmProjects/genesis/imgs/outfile.png"))
        self.file_label.setScaledContents(True)
        self.file_label.setObjectName("file_label")
        self.file_label.mousePressEvent = self.changeScreen

        # -----------  sales_tableWidget  -----------
        self.sales_tableWidget = QtWidgets.QTableWidget(self)
        self.sales_tableWidget.setGeometry(QtCore.QRect(0, 65, widgetWidth, widgetHeight - 115))
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
        self.sales_tableWidget.setColumnWidth(2, 90)
        self.sales_tableWidget.setColumnWidth(3, 250)
        self.sales_tableWidget.setColumnWidth(4, 40)
        self.sales_tableWidget.setColumnWidth(5, 65)
        self.sales_tableWidget.setColumnWidth(6, 50)
        self.sales_tableWidget.setColumnWidth(7, 75)
        self.sales_tableWidget.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.sales_tableWidget.horizontalHeader().setEnabled(False)
        self.sales_tableWidget.verticalHeader().hide()
        self.sales_tableWidget.setSelectionMode(1)  # 1 Single selection
        self.sales_tableWidget.setSelectionBehavior(1)  # 1 para selection de only rows
        self.sales_tableWidget.itemChanged.connect(self.changeIcon)
        self.change_color_criterio()
        self.retranslateUi()


        # -----------  bottom frame configuration  -----------
        self.botton_frame = QtWidgets.QFrame(self)
        self.botton_frame.setGeometry(QtCore.QRect(0, widgetHeight - 50, widgetWidth, 50))
        self.botton_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.botton_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.botton_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.botton_frame.setObjectName("botton_frame")

        # -----------  lblCash Configuration  -----------
        self.lblTitle_cash = QtWidgets.QLabel(self.botton_frame)
        self.lblTitle_cash.setGeometry(QtCore.QRect(607, 0, 360, 25))
        self.lblTitle_cash.setWordWrap(False)
        self.lblTitle_cash.setObjectName("lblTitle_cash")

        # -----------  lblCredit Configuration  -----------
        self.lblTitle_credit = QtWidgets.QLabel(self.botton_frame)
        self.lblTitle_credit.setGeometry(QtCore.QRect(610, 25, 360, 25))
        self.lblTitle_credit.setWordWrap(False)
        self.lblTitle_credit.setObjectName("lblTitle_credit")
        self.change_color_lbltitle()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbDate.setTitle(_translate("Dialog", "Fecha"))


        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(9)
        font.setWeight(65)
        font.setBold(True)

        item = self.sales_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("salesDialog", "id"))
        item.setFont(font)
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
        # self.gbCriterio.setPalette(palette)
        # self.gbCriterio.setFont(font)
        self.gbDate.setPalette(palette)
        self.gbDate.setFont(font)
        # self.gbBottom.setPalette(palette)
        # self.gbBottom.setFont(font)

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
        # self.lblTitle_items.setFont(font)
        # self.lblTitle_items.setPalette(palette)

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
    def widgetChanged(self, i):
        if i == 0 and self.ui_dialog_.addFlag:
            self.loadTable()
        elif i == 2:
            self.cust_dialog_.init_condition()
        elif i == 1:
            if self.cust_dialog_.saverFlag:
                self.ui_dialog_.custGest.fill_customers()
                self.ui_dialog_.loadCustomers()
                self.cust_dialog_.saverFlag = False

    def changeIcon(self, item):
        row = item.row()
        column = item.column()
        if self.sales_tableWidget.item(row, 6) != None and not self.loadFlag and column == 6:
            # try:
            cellValue = self.sales_tableWidget.item(row, 6).text().split("-")
            cellValue = cellValue[0:2]
            if cellValue[-1] == "":
                cellValue.pop(-1)
            if len(cellValue) == 2 and not self.loadFlag and self.sales_tableWidget.item(row, 0).text() == '0':
                if self.salesGest.changeReceipt(self.ownWares[0], self.salesTable[row].id_, str.upper(cellValue[0] + "-" + cellValue[1])):
                    self.salesTable[row].receipt = str.upper(cellValue[0] + "-" + cellValue[1])
                    self.salesTable[row].block = True
                    QMessageBox.question(self, 'Alerta', "Serie guardada",
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif len(cellValue) == 2 and not self.loadFlag and self.sales_tableWidget.item(row, 0).text() != '0':
                date = self.cmbDate.currentText().split("-")[2] + "-" + self.cmbDate.currentText().split("-")[1] \
                       + "-" + self.cmbDate.currentText().split("-")[0]
                if self.salesGest.changeReceipt(self.ownWares[0], self.salesTable[row].id_, str.upper(cellValue[0] + "-" + cellValue[1]),
                                                True, date, self.salesTable[row].id):
                    self.changesreceipt(self.salesTable[row].id, str.upper(cellValue[0] + "-" + cellValue[1]))
                    QMessageBox.question(self, 'Alerta', "Serie guardada",
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.salesTable[row].receipt = ""
                self.salesTable[row].block = False
            self.loadtableWidget()
        #
        #
            # else:
            #     pass
        #             if not self.loadFlag:
        #                 QMessageBox.question(self, 'Alerta', "Debe respetar el formato\n[B/F][NUMERO]-[NUMERO]", QMessageBox.Ok, QMessageBox.Ok)
        #                 self.loadFlag = True
        #                 self.sales_tableWidget.item(row, 6).setText(" ")
        #                 self.loadFlag = False
        #     except:
        #         QMessageBox.question(self, 'Alerta', "Debe respetar el formato\n[B/F][NUMERO]-[NUMERO]", QMessageBox.Ok, QMessageBox.Ok)
        #         self.loadFlag = True
        #         self.sales_tableWidget.item(row, 6).setText(" ")
        #         self.loadFlag = False

    def changesreceipt(self, id, receipt):
        for i in self.salesTable:
            if i.id == id:
                i.receipt = receipt
                i.block = True

class customer_Dialog(QtWidgets.QDialog):
    # def __init__(self, data_users = None, data_wares = None, parent=None):
    def __init__(self, widget, parent=None):
        super(customer_Dialog, self).__init__(parent)
        self.widget = widget
        self.setupUi()
        self.reniecGest = ApisNetPe(API_TOKEN)
        self.saverFlag = False
        self.customerGest = customer_gestor(True)

    def init_condition(self):
        self.txtDoc.clear()
        self.txtName.clear()
        self.txtPhone.clear()
        self.txtEmail.setEnabled(False)
        self.saverFlag = False
    def guardarUser(self):
        if self.txtDoc.text() != "" and self.txtName.text() != "" and self.txtPhone.text() != "":
            if self.customerGest.addCustomer(self.txtName.text(), self.txtDoc.text(), self.txtPhone.text()):
                QMessageBox.question(self, 'Alerta', "Cliente agregado", QMessageBox.Ok, QMessageBox.Ok)
                self.saverFlag = True
                self.gotoScreen1()
            else:
                QMessageBox.question(self, 'Alerta', "Falla en el sistema, contactar asistencia", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Alerta', "Debe llenar todos los campos",
                                 QMessageBox.Ok, QMessageBox.Ok)

    def buscar_User(self, event):
        if self.txtDoc.text() != "" and len(self.txtDoc.text()) == 8:
            response = self.reniecGest.get_person(self.txtDoc.text())
            if response != None:
                self.txtName.setText(response["nombre"])
            else:
                QMessageBox.question(self, 'Alerta', "No se obtuvo resultados",
                                     QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'Alerta', "Debe ingresar un numero de 8 digitos",
                                 QMessageBox.Ok, QMessageBox.Ok)
    def gotoScreen1(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

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
        self.gbNewUser.setPalette(palette)
        self.gbNewUser.setFont(font)

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
        self.lblDoc.setPalette(palette)
        self.lblName.setPalette(palette)
        self.lblPhone.setPalette(palette)
        self.lblemail.setPalette(palette)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbNewUser.setTitle(_translate("Dialog", "Nuevo Cliente"))
        self.lblDoc.setText(_translate("Dialog", "Documento:"))
        self.lblName.setText(_translate("Dialog", "Cliente:"))
        self.lblPhone.setText(_translate("Dialog", "Telefono:"))
        self.lblemail.setText(_translate("Dialog", "correo:"))


        self.lblDoc.adjustSize() #Ajusta el tamaño del label al tamaño de las letras
        self.lblName.adjustSize()
        self.lblPhone.adjustSize()
        self.lblemail.adjustSize()
        self.lblDoc.move(self.gbNewUser.width() - 300 - self.lblDoc.width(), 30) #cambia la posicion del label
        self.lblName.move(self.gbNewUser.width() - 300 - self.lblName.width(), 75)
        self.lblPhone.move(self.gbNewUser.width() - 300 - self.lblPhone.width(), 120)
        self.lblemail.move(self.gbNewUser.width() - 300 - self.lblemail.width(), 165)

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(widgetWidth, widgetHeight)
        self.setFixedSize(widgetWidth, widgetHeight)

        # -----------  back_frame configuration  -----------
        self.back_frame = QtWidgets.QFrame(self)
        self.back_frame.setGeometry(QtCore.QRect(0, 0, widgetWidth, widgetHeight)) #width 640, height 65
        self.back_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.back_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.back_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.back_frame.setObjectName("back_frame")


        # -----------  new customer configuration  -----------
        self.gbNewUser = QtWidgets.QGroupBox(self.back_frame)
        self.gbNewUser.setGeometry(QtCore.QRect(20, 20, 420, 420))
        self.gbNewUser.setObjectName("gbNewUser")
        self.change_color_criterio()

        # -----------  cuatro labeles , doc, name, telefono, correo  -----------
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblDoc = QtWidgets.QLabel(self.gbNewUser)
        self.lblDoc.setGeometry(QtCore.QRect(20, 30, 150, 30))
        self.lblDoc.setFont(font)
        self.lblDoc.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblDoc.setWordWrap(False)
        self.lblDoc.setObjectName("lblDoc")

        self.lblName = QtWidgets.QLabel(self.gbNewUser)
        self.lblName.setGeometry(QtCore.QRect(20, 75, 150, 30))
        self.lblName.setFont(font)
        self.lblName.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblName.setWordWrap(False)
        self.lblName.setObjectName("lblName")

        self.lblPhone = QtWidgets.QLabel(self.gbNewUser)
        self.lblPhone.setGeometry(QtCore.QRect(20, 120, 150, 30))
        self.lblPhone.setFont(font)
        self.lblPhone.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblPhone.setWordWrap(False)
        self.lblPhone.setObjectName("lblPhone")

        self.lblemail = QtWidgets.QLabel(self.gbNewUser)
        self.lblemail.setGeometry(QtCore.QRect(20, 165, 150, 30))
        self.lblemail.setFont(font)
        self.lblemail.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblemail.setWordWrap(False)
        self.lblemail.setObjectName("lblemail")
        self.change_color_lbltitle()

        # -----------  cuatro txt doc, name, telf, email  -----------
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(55)

        self.txtDoc = QtWidgets.QLineEdit(self.gbNewUser)
        self.txtDoc.setGeometry(QtCore.QRect(140, 30, 120, 30))
        self.txtDoc.setFont(font)
        self.txtDoc.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtDoc.setClearButtonEnabled(True)
        self.txtDoc.setObjectName("txtDoc")
        self.txtDoc.setPlaceholderText("Obligatorio")

        self.txtName = QtWidgets.QLineEdit(self.gbNewUser)
        self.txtName.setGeometry(QtCore.QRect(140, 75, 180, 30))
        self.txtName.setFont(font)
        self.txtName.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtName.setClearButtonEnabled(True)
        self.txtName.setObjectName("txtName")
        self.txtName.setPlaceholderText("Obligatorio")

        self.txtPhone = QtWidgets.QLineEdit(self.gbNewUser)
        self.txtPhone.setGeometry(QtCore.QRect(140, 120, 180, 30))
        self.txtPhone.setFont(font)
        self.txtPhone.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtPhone.setClearButtonEnabled(True)
        self.txtPhone.setObjectName("txtPhone")
        self.txtPhone.setPlaceholderText("Obligatorio (9 dig)")

        self.txtEmail = QtWidgets.QLineEdit(self.gbNewUser)
        self.txtEmail.setGeometry(QtCore.QRect(140, 165, 180, 30))
        self.txtEmail.setFont(font)
        self.txtEmail.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtEmail.setClearButtonEnabled(True)
        self.txtEmail.setObjectName("txtEmail")
        self.txtEmail.setPlaceholderText("Opcional")


        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)

        self.btnGuardar = QtWidgets.QPushButton('Guardar', self.gbNewUser)
        self.btnGuardar.setGeometry(56, 220, 100, 25)
        self.btnGuardar.setFont(font)
        self.btnGuardar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnGuardar.setAutoExclusive(True)
        self.btnGuardar.clicked.connect(self.guardarUser)

        self.btnRegresar = QtWidgets.QPushButton('Regresar', self.gbNewUser)
        self.btnRegresar.setGeometry(212, 220, 100, 25)
        self.btnRegresar.setFont(font)
        self.btnRegresar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnRegresar.setAutoExclusive(True)
        self.btnRegresar.clicked.connect(self.gotoScreen1)

        self.btnBuscarUser = QtWidgets.QPushButton('Buscar por Dni', self.gbNewUser)
        self.btnBuscarUser.setGeometry(275, 34, 120, 25)
        self.btnBuscarUser.setFont(font)
        self.btnBuscarUser.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnBuscarUser.setAutoExclusive(True)
        self.btnBuscarUser.clicked.connect(self.buscar_User)
        self.retranslateUi()




class user:
	def __init__(self, user = "", passwd = "", name = "", doc = "", phone = "", enabled = False):
		self.user = user
		self.passwd = passwd
		self.name = name
		self.doc = doc
		self.phone = phone
		self.enabled = enabled


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog_ = QDialog()
    obj1 = user("admin01", "chuspa", "IVAN ROJAS CARRASCO", "72732900", "993324631", True)
    obj2 = user("ventas01", "catalina", " ", " ", " ", True)
    users = []
    users.append(obj1)
    users.append(obj2)
    date_users  = (obj1, users)

    ware_List = ["ALYZ", "SNTG", "STC"]
    users = ["hola mundo", ("catalina", "chuspa")]
    ui_dialog = sales_Dialog(date_users, ware_List, dialog_)
    ui_dialog.init_condition()
    ui_dialog.widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")
