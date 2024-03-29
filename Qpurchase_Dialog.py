
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gestor import supplier_gestor, purchase_gestor
from PyQt5.QtWidgets import QCompleter, QHeaderView, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication


widgetHeight = 500
widgetWidth = 710

class Validator(QtGui.QValidator):
    def validate(self, string, pos):
        return QtGui.QValidator.Acceptable, string.upper(), pos

class Ui_Qpurchase(QtWidgets.QDialog):
    def __init__(self, data_users = None, data_wares = None, parent=None):
        super(Ui_Qpurchase, self).__init__(parent)
        self.supplier_gest = supplier_gestor() #gestor para proveedores
        self.purchase_gest = purchase_gestor() #gestor para compras
        #
        self.ownUsers = data_users
        self.ownWares = data_wares
        self.setupUi() #configuracion de GUI
        #
        #declaracion de variables locales o de clase
        self.purchase_list = []

    def updateTable(self):
        self.purchase_table.blockSignals(True)
        self.purchase_list.clear()
        self.purchase_table.clearContents()
        flag1 = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        self.purchase_list = self.purchase_gest.list_purchases.copy()
        # -----------  esta parte para llenar la tabla  -----------
        row = 0
        self.purchase_table.setRowCount(len(self.purchase_list))
        font = QtGui.QFont("Open Sans Semibold", pointSize=10, weight=60)

        for p in self.purchase_list:
            item = QtWidgets.QTableWidgetItem(p.inputDate)
            item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            self.purchase_table.setItem(row, 0, item)
            #
            item = QtWidgets.QTableWidgetItem(p.inputWare)
            item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            self.purchase_table.setItem(row, 1, item)
            #
            item = QtWidgets.QTableWidgetItem(p.user)
            item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            self.purchase_table.setItem(row, 2, item)
            #
            item = QtWidgets.QTableWidgetItem(p.type)
            item.setFlags(flag)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            self.purchase_table.setItem(row, 3, item)
            #
            item = QtWidgets.QTableWidgetItem(p.serie)
            item.setFlags(flag1)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(font)
            self.purchase_table.setItem(row, 4, item)
            #
            if p.type == "CREDITO":
                itemBtn = QPushButton("PAGAR")
                itemBtn.clicked.connect(self.btnCellClicked)
                itemBtn.setFont(font)
                self.purchase_table.setCellWidget(row, 5, itemBtn)
            #
            pbar = QProgressBar()
            tmp_val = round((p.payment/p.debt)*100)
            pbar.setFixedWidth(130)
            pbar.setFont(font)
            pbar.setValue(tmp_val)
            self.purchase_table.setCellWidget(row, 6, pbar)
            row += 1
        self.purchase_table.blockSignals(False)

    def consultar(self):
        self.top_frame.setEnabled(False)
        self.purchase_gest.getPurchasesxSupplier(self.txtBusqueda.text().split("|")[4].strip())
        self.updateTable()

    def show(self):
        self.init_condition()
        self.open()

    def init_condition(self):
        self.btnConsultar.setEnabled(False)
        self.updateQcompleter()
        self.txtBusqueda.clear()
        self.txtDoc.clear()
        self.txtCompanyName.clear()
        self.txtSeller.clear()
        self.purchase_table.clearContents()

    def introSupplier(self, selectedOption):
        if len(self.txtBusqueda.text().split("|")) > 1:
            self.txtDoc.setText(self.txtBusqueda.text().split("|")[1].strip())
            self.txtCompanyName.setText(self.txtBusqueda.text().split("|")[0].strip())
            self.txtSeller.setText(self.txtBusqueda.text().split("|")[3].strip() + " | " + self.txtBusqueda.text().split("|")[2].strip())
            QTimer.singleShot(0, lambda: self.txtBusqueda.home(False))
            QTimer.singleShot(0, lambda: self.txtCompanyName.home(False))
            QTimer.singleShot(0, lambda: self.txtSeller.home(False))

    def txtchanged(self, dato):
        if dato == "":
            self.txtDoc.clear()
            self.txtCompanyName.clear()
            self.txtSeller.clear()
            self.purchase_table.setRowCount(0)
        if len(self.txtBusqueda.text().split("|")) == 5:
            self.btnConsultar.setEnabled(True)
        else:
            self.btnConsultar.setEnabled(False)

    def updateQcompleter(self):
        supplier_list = []
        self.supplier_gest.fill_suppliers()
        for i in self.supplier_gest.suppliers:
            supplier_list.append(str(i.name) + " | " + str(i.main_doc) + " | " + str(i.name_admin)
                                      + " | " + str(i.doc_admin) + " | " + str(i.cod))
        model = self.completer.model()
        model.removeRows(0, model.rowCount())
        model.setStringList(supplier_list)

    def activateTopFrame(self, event):
        self.top_frame.setEnabled(True)

    def btnCellClicked(self):
        # find what is clicked
        clicked = QApplication.focusWidget()
        # position
        # idx = self.purchase_table.indexAt(clicked.pos())
        row = self.purchase_table.indexAt(clicked.pos()).row()
        # item.clicked.connect(lambda: print("Hola Mundo"))
        ##aca se va revisar si en caso se pago de otro lado, recomendable que lo haga un user
        availableDebt = self.purchase_list[row].debt - self.purchase_list[row].payment
        paymentUI = Ui_Qdopayment(self.ownUsers, availableDebt)
        if  paymentUI.exec_() == QtWidgets.QDialog.Accepted:
            pass
            # print("Hola Mundo")
            # self.setEnabled(True)
            # self.isopenware = False
            # self.isupdateWare = False
            # print(idx.row())

    def itemContentChanged(self, item):
        if item.column() == 4:
            self.purchase_gest.updateSerie(item.text(), self.purchase_list[item.row()].id)

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(Ui_Qdopayment, self).keyPressEvent(event)

    def setupUi(self):
        self.setObjectName("QpurchaseDialog")
        self.resize(widgetWidth, widgetHeight)
        self.setFixedSize(widgetWidth, widgetHeight)

        # -----------  top frame configuration  -----------
        self.top_frame = QtWidgets.QFrame(self)
        self.top_frame.setGeometry(QtCore.QRect(0, 0, widgetWidth, 145)) #width 640, height 95
        self.top_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.top_frame.setObjectName("top_frame")

        self.tmp_frame = QtWidgets.QFrame(self)
        self.tmp_frame.setGeometry(QtCore.QRect(0, 110, widgetWidth - 160, 35))  # width 640, height 95
        self.tmp_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 0), stop:1 rgba(97, 69, 128, 0));")
        self.tmp_frame.mousePressEvent = self.activateTopFrame

        # # -----------  groupBox configuration  -----------
        self.gbSuppliers = QtWidgets.QGroupBox(self.top_frame)
        self.gbSuppliers.setGeometry(QtCore.QRect(10, 0, 688, 100))
        # self.change_color_criterio() #funcion que cambia color y fuente de gbSuppliers
        self.gbSuppliers.setObjectName("gbSuppliers")

        # -----------  Qline buscadorproveedor configuration  -----------
        self.txtBusqueda = QtWidgets.QLineEdit(self.gbSuppliers)
        self.txtBusqueda.setGeometry(QtCore.QRect(95, 27, 320, 27))
        font = QtGui.QFont("Open Sans Semibold", pointSize = 11, weight = 60)
        self.txtBusqueda.setFont(font)
        self.txtBusqueda.setStyleSheet("background-color: rgb(248, 248, 248);")
        self.txtBusqueda.setClearButtonEnabled(True)
        self.txtBusqueda.setObjectName("txtBusqueda")
        self.txtBusqueda.setEnabled(True)
        self.txtBusqueda.textChanged.connect(self.txtchanged)
        #
        self.validator = Validator()
        self.txtBusqueda.setValidator(self.validator)

        self.completer = QCompleter(["IVAN ALEXIS", "ROJAS CARRASCO"], self.txtBusqueda)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.introSupplier)
        self.txtBusqueda.setCompleter(self.completer)

        # -----------  Qline numero de documento configuration  -----------
        self.txtDoc = QtWidgets.QLineEdit(self.gbSuppliers)
        self.txtDoc.setGeometry(QtCore.QRect(515, 27, 165, 27))
        self.txtDoc.setFont(font)
        self.txtDoc.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtDoc.setObjectName("txtDoc")
        self.txtDoc.setEnabled(False)
        #
        # -----------  Qline nombre de empresa configuration  -----------
        self.txtCompanyName = QtWidgets.QLineEdit(self.gbSuppliers)
        self.txtCompanyName.setGeometry(QtCore.QRect(95, 60, 320, 27))
        self.txtCompanyName.setFont(font)
        self.txtCompanyName.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtCompanyName.setObjectName("txtCompanyName")
        self.txtCompanyName.setEnabled(False)
        #
        # -----------  Qline responsable configuration  -----------
        self.txtSeller = QtWidgets.QLineEdit(self.gbSuppliers)
        self.txtSeller.setGeometry(QtCore.QRect(515, 60, 165, 27))
        self.txtSeller.setFont(font)
        self.txtSeller.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.txtSeller.setObjectName("txtCompanyName")
        self.txtSeller.setEnabled(False)
        #
        # # -----------  lblbuscadorproveedor configuration  -----------
        self.lblProveedor = QtWidgets.QLabel(self.gbSuppliers)
        self.lblProveedor.setGeometry(QtCore.QRect(10, 25, 80, 31))
        font = QtGui.QFont("Open Sans Semibold", pointSize = 12, weight = 65)
        self.lblProveedor.setFont(font)
        self.lblProveedor.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblProveedor.setWordWrap(False)
        #
        # # -----------  lbl dccumento proveedor configuration  -----------
        self.lblDoc = QtWidgets.QLabel(self.gbSuppliers)
        self.lblDoc.setGeometry(QtCore.QRect(440, 25, 80, 31))
        self.lblDoc.setFont(font)
        self.lblDoc.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblDoc.setWordWrap(False)
        #
        # # -----------  lblbuscadorproveedor configuration  -----------
        self.lblCompanyName = QtWidgets.QLabel(self.gbSuppliers)
        self.lblCompanyName.setGeometry(QtCore.QRect(10, 60, 80, 31))
        self.lblCompanyName.setFont(font)
        self.lblCompanyName.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblCompanyName.setWordWrap(False)
        #
        # # -----------  lblbuscadorproveedor configuration  -----------
        self.lblSellerName = QtWidgets.QLabel(self.gbSuppliers)
        self.lblSellerName.setGeometry(QtCore.QRect(427, 60, 80, 31))
        self.lblSellerName.setFont(font)
        self.lblSellerName.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblSellerName.setWordWrap(False)

        # # -----------  groupBox btn consultar configuration  -----------
        self.gbBtnConsultar = QtWidgets.QGroupBox(self.top_frame)
        self.gbBtnConsultar.setGeometry(QtCore.QRect(588, 103, 110, 40))
        # self.change_color_criterio() #funcion que cambia color y fuente de gbSuppliers
        self.gbBtnConsultar.setObjectName("gbSuppliers")

        # # -----------  consultar Button  -----------
        self.btnConsultar = QtWidgets.QPushButton("Consultar", self.gbBtnConsultar)
        self.btnConsultar.setGeometry(5, 5, 100, 30)
        font = QtGui.QFont("Open Sans Semibold", pointSize=11, weight=75)
        self.btnConsultar.setFont(font)
        self.btnConsultar.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.btnConsultar.clicked.connect(self.consultar)
        #
        # -----------  in_tableWidget  -----------
        self.purchase_table = QtWidgets.QTableWidget(self)
        self.purchase_table.setGeometry(QtCore.QRect(0, 145, widgetWidth, 355))
        self.purchase_table.setObjectName("purchase_table")
        self.purchase_table.setColumnCount(7)
        self.purchase_table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem())
        self.purchase_table.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem())
        self.purchase_table.setColumnWidth(0, 95)
        self.purchase_table.setColumnWidth(1, 80)
        self.purchase_table.setColumnWidth(2, 85)
        self.purchase_table.setColumnWidth(3, 110)
        self.purchase_table.setColumnWidth(4, 75)
        self.purchase_table.setColumnWidth(5, 130)
        self.purchase_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.purchase_table.verticalHeader().hide()
        self.purchase_table.setSelectionMode(1)
        self.purchase_table.setSelectionBehavior(1)
        self.purchase_table.horizontalHeader().setEnabled(False)
        self.purchase_table.itemChanged.connect(self.itemContentChanged)
        #
        self.change_color_lbltitle()
        self.change_color_criterio()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))
        self.gbSuppliers.setTitle(_translate("inoutDialog", "Cuadro de busqueda"))
        self.lblProveedor.setText(_translate("inoutDialog", "Buscador: "))
        self.lblDoc.setText(_translate("inoutDialog", "Ruc/Dni:"))
        self.lblCompanyName.setText(_translate("inoutDialog", "R. Social:"))
        self.lblSellerName.setText(_translate("inoutDialog", "Vendedor:"))

        font = QtGui.QFont("Open Sans Semibold", pointSize=11, weight=85)
        font.setBold(True)
        item = self.purchase_table.horizontalHeaderItem(0)
        item.setText(_translate("inoutDialog", "fecha ing."))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(1)
        item.setText(_translate("inoutDialog", "almacen"))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(2)
        item.setText(_translate("inoutDialog", "usuario"))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(3)
        item.setText(_translate("inoutDialog", "tipo"))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(4)
        item.setText(_translate("inoutDialog", "serie"))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(5)
        item.setText(_translate("inoutDialog", "operación"))
        item.setFont(font)
        item = self.purchase_table.horizontalHeaderItem(6)
        item.setText(_translate("inoutDialog", "estado"))
        item.setFont(font)

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
        self.lblProveedor.setPalette(palette)
        self.lblDoc.setPalette(palette)
        self.lblCompanyName.setPalette(palette)
        self.lblSellerName.setPalette(palette)

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
        font = QtGui.QFont("Open Sans Semibold", pointSize=11, weight=75)
        font.setBold(True)
        self.gbSuppliers.setPalette(palette)
        self.gbSuppliers.setFont(font)



class Ui_Qdopayment(QtWidgets.QDialog):
    def __init__(self, data_users = None, availableDebt = 0.0, parent=None):
        super(Ui_Qdopayment, self).__init__(parent)
        #
        self.ownUsers = data_users
        self.setupUi() #configuracion de GUI
        #
        #localvariables
        self.currentDebt = availableDebt
        #initfunctions
        self.initConditions()
    def closeEvent(self, event):
        self.accept()
        event.accept()

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(Ui_Qdopayment, self).keyPressEvent(event)
        else:
            self.accept()
            event.accept()

    def initConditions(self):
        self.lblDeuda = QtWidgets.QLabel(self)
        self.lblDeuda.setGeometry(QtCore.QRect(10, 25, 150, 31))
        font = QtGui.QFont("Open Sans Semibold", pointSize = 12, weight = 65)
        self.lblDeuda.setFont(font)
        self.lblDeuda.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblDeuda.setText("Deuda: " + str(self.currentDebt))

    def setupUi(self):
        self.setObjectName("Ui_Qdopayment")
        self.setFixedSize(410, 150)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Qpurchase()
    ui.show()
    app.exec_()
