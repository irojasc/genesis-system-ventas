import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from gestor import ware_gestor, wares_gestor
from inout_dialog import Ui_inoutDialog

class sales_Dialog(QtWidgets.QDialog):
    def __init__(self, data_users = None, data_wares = None, parent=None):
        super(sales_Dialog, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(640, 360)
        self.setFixedSize(640, 360)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Genesis - [Museo del libro]"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog_ = QDialog()
    ui_dialog = sales_Dialog(None, None, dialog_)
    ui_dialog.exec_()
    # app.exec_()
