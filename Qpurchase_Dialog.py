
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import QFont, QBrush, QColor
# from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
# from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
# from PyQt5.QtWidgets import *
# from gestor import ware_gestor, transfer



class Ui_Qpurchase(QtWidgets.QDialog):
    def __init__(self, data_users = None, data_wares = None, parent=None):
        super(Ui_Qpurchase, self).__init__(parent)
        self.setupUi()
        pass
        # self.ownUsers = data_users
        # self.ownWares = data_wares
        # self.mainList = []
        # self.duobleClickFlag = False
        # self.main_table = []
        # self.cantItems = 0
        # self.finalWare = ""
        # self.ware_in = ware_gestor() #esto es para realizar el update
        # self.trasferGest = transfer() # esto es para realizar transferencias
        # self.setupUi()
        # self.init_condition()

    def setupUi(self):
        self.setObjectName("QpurchaseDialog")
        self.resize(640, 360)
        self.setFixedSize(640, 360)
        # -----------  top frame configuration  -----------
        self.top_frame = QtWidgets.QFrame(self)
        self.top_frame.setGeometry(QtCore.QRect(0, 0, 640, 65)) #width 640, height 65
        self.top_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(83, 97, 142, 255), stop:1 rgba(97, 69, 128, 255));")
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName("top_frame")

        # # -----------  groupBox configuration  -----------
        # self.gbCriterio = QtWidgets.QGroupBox(self.top_frame)
        # self.gbCriterio.setGeometry(QtCore.QRect(20, 0, 390, 60))
        # #self.change_color_criterio() #funcion que cambia color y fuente de gbCriterio
        # self.gbCriterio.setObjectName("gbCriterio")
        #
        # # -----------  QComboBox configuration  -----------
        # self.cmbBusqueda = QtWidgets.QComboBox(self.gbCriterio)
        # self.cmbBusqueda.setGeometry(QtCore.QRect(10, 23, 80, 30))
        # self.cmbBusqueda.setStyleSheet("background-color: rgb(170, 255, 0);")
        # font = QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(10)
        # font.setBold(True)
        # font.setWeight(75)
        # self.cmbBusqueda.setFont(font)
        # self.cmbBusqueda.setObjectName("cmbBusqueda")
        # self.cmbBusqueda.currentIndexChanged.connect(self.onCmbIndexChanged)
        #
        # # -----------  QlineWidget configuration  -----------
        # self.txtBusqueda = QtWidgets.QLineEdit(self.gbCriterio)
        # self.txtBusqueda.setGeometry(QtCore.QRect(100, 23, 280, 30))
        # font = QtGui.QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)
        # self.txtBusqueda.setFont(font)
        # self.txtBusqueda.setStyleSheet("background-color: rgb(248, 248, 248);")
        # self.txtBusqueda.setClearButtonEnabled(True)
        # self.txtBusqueda.setObjectName("txtBusqueda")
        # self.txtBusqueda.textChanged.connect(self.txtBusquedaChanged)
        # self.txtBusqueda.keyPressEvent = self.txtbusquedaAcept
        #
        # # -----------  lbl final ware configuration  -----------
        # self.lblTitle = QtWidgets.QLabel(self.top_frame)
        # self.lblTitle.setGeometry(QtCore.QRect(450, 19, 361, 31))
        # font = QtGui.QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(12)
        # font.setBold(True)
        # font.setWeight(75)
        # self.lblTitle.setFont(font)
        # self.lblTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.lblTitle.setWordWrap(False)
        # self.lblTitle.setObjectName("lblTitle")
        #
        # # -----------  qlist configuration  -----------
        # self.searchList = QtWidgets.QListWidget(self)
        # self.searchList.setGeometry(QtCore.QRect(0, 65, 640, 65))
        # font = QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(10)
        # font.setBold(False)
        # font.setWeight(45)
        # self.searchList.setFont(font)
        # self.searchList.setObjectName("searchList")
        # self.searchList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.searchList.keyPressEvent = self.listSearchKey
        #
        # # -----------  mid-frame configuration  -----------
        # self.mid_frame = QtWidgets.QFrame(self)
        # self.mid_frame.setGeometry(QtCore.QRect(0, 130, 640, 5)) #width 640, height 65
        # self.mid_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(22, 136, 126, 255), stop:1 rgba(56, 110, 142, 255));")
        # self.mid_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.mid_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.mid_frame.setObjectName("mid_frame")
        #
        #
        # # -----------  in_tableWidget  -----------
        # self.in_tableWidget = QtWidgets.QTableWidget(self)
        # self.in_tableWidget.setGeometry(QtCore.QRect(0, 135, 640, 175))
        # self.in_tableWidget.setObjectName("in_tableWidget")
        # self.in_tableWidget.setColumnCount(4)
        # self.in_tableWidget.setRowCount(0)
        # item = QtWidgets.QTableWidgetItem()
        # self.in_tableWidget.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.in_tableWidget.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.in_tableWidget.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.in_tableWidget.setHorizontalHeaderItem(3, item)
        #
        # self.in_tableWidget.setColumnWidth(0,80)
        # self.in_tableWidget.setColumnWidth(1,120)
        # self.in_tableWidget.setColumnWidth(2,365)
        # self.in_tableWidget.setColumnWidth(3,75)
        # self.in_tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        # self.in_tableWidget.horizontalHeader().setEnabled(False)
        # self.in_tableWidget.setSelectionMode(1)
        # self.in_tableWidget.setSelectionBehavior(1)
        # self.in_tableWidget.setStyleSheet("selection-background-color: rgb(0, 120, 255);selection-color: rgb(255, 255, 255);")
        # self.in_tableWidget.verticalHeader().hide()
        # self.in_tableWidget.keyPressEvent = self.KeyPressed
        # self.in_tableWidget.itemChanged.connect(self.changeIcon)
        # #self.in_tableWidget.itemDoubleClicked.connect(self.doubleClickItem)
        #
        # # -----------  bottom frame configuration  -----------
        # self.frame = QtWidgets.QFrame(self)
        # self.frame.setGeometry(QtCore.QRect(0, 310, 640, 50))
        # self.frame.setStyleSheet(
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0.298507 rgba(22, 136, 126, 255), stop:1 rgba(56, 110, 142, 255));")
        # self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame.setObjectName("frame")
        #
        # # -----------  lblCantidad Configuration  -----------
        # self.lblTitle_cant = QtWidgets.QLabel(self.frame)
        # self.lblTitle_cant.setGeometry(QtCore.QRect(520, 12, 391, 31))
        # self.change_color_lbltitle()
        # self.lblTitle_cant.setWordWrap(False)
        # self.lblTitle_cant.setObjectName("lblTitle_cant")
        #
        # # -----------  groupBoxBottom configuration  -----------
        # self.gbBottom = QtWidgets.QGroupBox(self.frame)
        # self.gbBottom.setGeometry(QtCore.QRect(5, 5, 110, 40))
        # self.change_color_criterio() #funcion que cambia color y fuente de gbCriterio
        # self.gbBottom.setObjectName("gbBottom")
        #
        #
        # # -----------  btn aceptar configutarion  -----------
        # self.btnAceptar = QtWidgets.QPushButton(self.gbBottom)
        # self.btnAceptar.setGeometry(QtCore.QRect(5, 5, 100, 30))
        # font = QtGui.QFont()
        # font.setFamily("Open Sans Semibold")
        # font.setPointSize(11)
        # font.setBold(True)
        # font.setWeight(75)
        # self.btnAceptar.setFont(font)
        # self.btnAceptar.setStyleSheet("background-color: rgb(240, 240, 240);")
        # self.btnAceptar.setObjectName("btnAceptar")
        # self.btnAceptar.setAutoExclusive(True)
        # self.btnAceptar.mousePressEvent = self.aceptarEvent

        # self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Qpurchase()
    ui.show()
    app.exec_()
