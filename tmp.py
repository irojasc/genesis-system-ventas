import sys
from PyQt5.QtWidgets import *


# Main Window
"""class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'VENTANA DE PRUEBA - ROCACODE'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show window
        self.show()

    # Create table
    def createTable(self):
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(4)

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3, 0, QTableWidgetItem("Arnavi"))
        self.tableWidget.item(3, 0).setToolTip("MIGUEL ROJAS")
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Mandsaur"))
        self.tableWidget.item(3,1).setToolTip("GN_1 DICCINARIO AKAL , CANT: 2\n GN_6 INCAS Y FARAONE, CANT: 5\n GN_21 VIAJAR")

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)"""

#def crear_Diccionario():
    #list = []
    #text = '0'
    #print(text)
    #print(bool(text))
    #dict = {'Nombre': "Ivan", 'Apellido': "Rojas"}
    #dict_ = {'Nombre': "Rick", 'Apellido': "Carrasco"}
    #dict__ = {'Nombre': "Rick", 'Apellido': "Carrasco"}
    #list.append(dict)
    #list.append(dict_)
    #list.append(dict__)
    #index = next((index for (index, d) in enumerate(list) if d["Nombre"] == "Rick"), None)
    # print(index)
    #test_list = ['3', '5', '7', '9', '11']

    # printing original list

    # using append() + pop() + index()
    # moving element to end
    #tmp = test_list.pop(test_list.index('7'))
    #test_list.insert(0,test_list.pop(test_list.index('7')))

    # printing result
    #print(str(test_list), len(test_list))


"""
from PyQt5 import QtCore, QtWidgets
import numpy as np

class HorizontalHeader(QtWidgets.QHeaderView):
    def __init__(self, values, parent=None):
        super(HorizontalHeader, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setSectionsMovable(True)
        self.comboboxes = []
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)

    def showEvent(self, event):
        for i in range(self.count()):
            if i < len(self.comboboxes):
                combo = self.comboboxes[i]
                combo.clear()
                combo.addItems(["Variable", "Timestamp"])
            else:
                combo = QtWidgets.QComboBox(self)
                combo.addItems(["Variable", "Timestamp"])
                self.comboboxes.append(combo)

            combo.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 4, self.height())
            combo.show()

        if len(self.comboboxes) > self.count():
            for i in range(self.count(), len(self.comboboxes)):
                self.comboboxes[i].deleteLater()

        super(HorizontalHeader, self).showEvent(event)

    def handleSectionResized(self, i):
        for i in range(self.count()):
            j = self.visualIndex(i)
            logical = self.logicalIndex(j)
            self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical) - 4,self.height())

    def handleSectionMoved(self, i, oldVisualIndex, newVisualIndex):
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            self.comboboxes[i].setGeometry(self.ectionViewportPosition(logical), 0, self.sectionSize(logical) - 5,
                                               height())

    def fixComboPositions(self):
        for i in range(self.count()):
            self.comboboxes[i].setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 5,
                                               self.height())

class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        header = HorizontalHeader(self)
        self.setHorizontalHeader(header)

    def scrollContentsBy(self, dx, dy):
        super(TableWidget, self).scrollContentsBy(dx, dy)
        if dx != 0:
            self.horizontalHeader().fixComboPositions()

class App(QtWidgets.QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.data = np.random.rand(10, 10)
        self.createTable()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        self.showMaximized()

    def createTable(self):
        self.header = []
        self.table = TableWidget(*self.data.shape)
        for i, row_values in enumerate(self.data):
            for j, value in enumerate(row_values):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    #App.show()
    #app.exec_()
    sys.exit(app.exec_())


#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = App()
    #sys.exit(app.exec_())
#    crear_Diccionario() """

"""
import sys
from PyQt5 import QtWidgets, QtCore

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(400,50,200,200)

        self.pushButton = QtWidgets.QPushButton('show messagebox', self)
        self.pushButton.setGeometry(25, 90, 150, 25)
        self.pushButton.clicked.connect(self.onClick)

    def onClick(self):
        #ret = QMessageBox.question(self, 'MessageBox', "Click a button", QMessageBox.Ok, QMessageBox.Ok)
        text, validation = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña de usuario",QtWidgets.QLineEdit.Password)
        #msgbox = QtWidgets.QMessageBox()
        #msgbox.setText('to select click "show details"')
        #msgbox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) # (QtCore.Qt.TextSelectableByMouse)
        #msgbox.setDetailedText('line 1\nline 2\nline 3')
        #msgbox.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_()) 

import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.setGeometry(1050, 500, 400, 50)
        self.setWindowTitle("Add")

    def initUI(self):
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)

        self.deckButton = QtWidgets.QPushButton()
        self.deckButton.setText("Choose")
        self.deckButton.clicked.connect(self.open_deck_browser)

        box = QtWidgets.QVBoxLayout(central)
        box.addWidget(self.deckButton)
        self.label = QtWidgets.QLabel()
        box.addWidget(self.label)
        self.label.hide()

    def open_deck_browser(self):
        dialog = DeckDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.label.show()
            self.label.setText(dialog.selected_text)

        #time.sleep(3)
        #self.label.setVisible(False)


class DeckDialog(QtWidgets.QDialog):
    def __init__(self):
        super(DeckDialog, self).__init__()

        self.initUI()
        self.setGeometry(200, 200, 800, 640)
        self.setWindowTitle("Choose Deck")

    def initUI(self):
        self.deckList = QtWidgets.QListWidget()

        self.deckList.insertItem(0, "GN_1001 | 9788497778213 | PIENSE Y HAGASE RICO | NAPOLEON HILL | OBELISCO")
        self.deckList.insertItem(1, "GN_372 | 9786124579257 | COMENTARIOS REALES DE LOS INCAS | GARCILASO DE LA VEGA | EL LECTOR")
        self.deckList.insertItem(2, "Hello There")
        self.deckList.insertItem(3, "Hello everybody")
        self.deckList.insertItem(4, "Bye Bye")

        self.deckList.item(1).setSelected(True)

        self.selectDeck = QtWidgets.QPushButton(self)
        self.selectDeck.setText("Choose")

        hboxCreateBottomButtons = QtWidgets.QHBoxLayout()

        hboxCreateBottomButtons.addStretch()
        hboxCreateBottomButtons.addWidget(self.selectDeck)

        vboxMain = QtWidgets.QVBoxLayout(self)
        vboxMain.addWidget(self.deckList)
        vboxMain.addLayout(hboxCreateBottomButtons)

        self.selectDeck.clicked.connect(self.accept)

    @property
    def selected_text(self):
        items = self.deckList.selectedItems()
        if items:
            return items[0].text()
        return ""


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 400, 200)
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton(self)
        self.button1.setGeometry(40, 40, 100, 50)
        self.button1.setText("Button 1")

        #self.button2 = QPushButton(self)
        #self.button2.setGeometry(150, 40, 100, 50)
        #self.button2.setText("Button 2")

        #self.btn_grp = QButtonGroup()
        #self.btn_grp.(True)
        #self.btn_grp.addButton(self.button1)
        #self.btn_grp.addButton(self.button2)

        #self.btn_grp.buttonClicked.connect(self.on_click)
        self.button1.clicked.connect(self.on_click)

        self.show()

    def on_click(self, btn):
        print("Hola Mundo")
        #pass # do something with the button clicked

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

*********************************************************************
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.openAction = QtWidgets.QAction('About', self)
        self.openAction.triggered.connect(self.aboutDialog)
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.setCentralWidget(self.calendar)

    def aboutDialog(self):
        self._about = AboutDialog(self)
        self.setDisabled (True)
        self._about.show()

    def enableWidgets(self):
        self.setDisabled(False)

class AboutDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)

        self.setMinimumSize(400, 350)

    def closeEvent(self, parent):
        self.parent().enableWidgets()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                self.parent().showMinimized()
            else:
                self.parent().showMaximized()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app_window = MainWindow()
    app_window.showMaximized()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QCheckBox, QApplication)
from PyQt5 import QtCore


class basicWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.checkBoxA = QCheckBox("Select This.")
        self.labelA = QLabel("Not slected.")

        self.checkBoxA.stateChanged.connect(self.checkBoxChangedAction)

        layout.addWidget(self.checkBoxA)
        layout.addWidget(self.labelA)

        self.setGeometry(200, 200, 300, 200)

        self.setWindowTitle('CheckBox Example')

    def checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.labelA.setText("Selected.")
        else:
            self.labelA.setText("Not Selected.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):
        # creating spin box
        self.spin = QSpinBox(self)

        # setting geometry to spin box
        self.spin.setGeometry(100, 100, 100, 40)

        # setting value to the spin box
        self.spin.setValue(20)


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

window.show()

# start the app
sys.exit(App.exec()) 

# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):
        # creating the check-box
        checkbox = QCheckBox('Geek ?', self)
        #checkbox = QCheckBox(self)

        # setting geometry of check box
        checkbox.setGeometry(200, 150, 13, 13)

        # setting stylesheet
        # changing width and height of indicator
        #checkbox.setStyleSheet("QCheckBox::indicator"
        #                       "{"
        #                       "width :100px;"
        #                       "height : 100px;"
        #                       "}")
        print(checkbox.width(),checkbox.height())


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec()) """
"""
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        #cbutton = QCheckBox("I have a Cat")
        cbutton = QCheckBox()
        cbutton.animal = "Cat"
        cbutton.toggled.connect(self.onClicked)
        layout.addWidget(cbutton, 0, 0)

    def onClicked(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña de usuario", QtWidgets.QLineEdit.Password)
            if text_ == "hola":
                print("Mensaje confirma que esta chequeado")
            else:
                cbutton.setChecked(False)
        if not cbutton.isChecked():
            print("Mensaje confirma que no esta chequeado")

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
# from datetime import datetime

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

# class CustomDialog(QtWidgets.QMainWindow):
#     def __init__(self, parent = None):
#         super(CustomDialog, self).__init__(parent)
#
#         self.setObjectName("LoginWindow")
#         self.resize(380, 312)
#         self.setFixedSize(380,312)
#
#         # -----------  Login Button  -----------
#         self.pushButton = QtWidgets.QPushButton(self)
#         self.pushButton.setEnabled(True)
#         self.pushButton.setGeometry(QtCore.QRect(70, 240, 230, 40))
#         font = QtGui.QFont()
#         font.setFamily("Open Sans")
#         font.setPointSize(11)
#         self.pushButton.setFont(font)
#         self.pushButton.setAutoFillBackground(False)
#         self.pushButton.setStyleSheet("background-color: rgb(189, 189, 189);\n"
#                                       "")
#         self.pushButton.setIconSize(QtCore.QSize(300, 50))
#         self.pushButton.setCheckable(False)
#         self.pushButton.setAutoRepeat(False)
#         self.pushButton.setAutoExclusive(False)
#         self.pushButton.setAutoDefault(False)
#         self.pushButton.setDefault(False)
#         self.pushButton.setFlat(False)
#         self.pushButton.setObjectName("pushButton")
#         self.pushButton.clicked.connect(self.inputDialogEvent)
#         self.setup()
#
#         self.label = QtWidgets.QLabel(self)
#         self.label.setGeometry(QtCore.QRect(55, 30, 270, 54))
#         self.label.setStyleSheet("")
#         self.label.setText("")
#         #self.label.setPixmap(QtGui.QPixmap("C:/Users/IROJAS/Desktop/Genesis/UI_STNG/imgs/login_user.png"))
#         #self.label.setScaledContents(True)
#         self.label.setObjectName("label")
#
#         #self.pushButton.clicked.connect(self.openMainWindow)
#         self.pushButton.setText("Log in")
#
#     def inputDialogEvent(self):
#         # text_, validation_ = QtWidgets.QInputDialog.getText(self, 'Validar operación', "Ingrese contraseña",
#         #                                                     QtWidgets.QLineEdit.Password)
#         self.inputext.open()
#         #self.inputext.textValue()
#         print(self.inputext.textValue())
#
#     def holaMundo(self):
#         print("Hola Mundo")
#
#         #self.inputext.setEnabled(False)
#     def setup(self):
#         self.inputext = QtWidgets.QInputDialog(self)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


def window():
    app = QApplication(sys.argv)
    win = QWidget()
    button1 = QPushButton(win)
    button1.setText("Show dialog!")
    button1.move(50, 50)
    button1.clicked.connect(showDialog)
    win.setWindowTitle("Click button")
    win.show()
    sys.exit(app.exec_())


def showDialog():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Message box pop up window")
    msgBox.setWindowTitle("QMessageBox Example")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.buttonClicked.connect(msgButtonClick)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        print('OK clicked')


def msgButtonClick(i):
    print("Button clicked is:", i.text())


if __name__ == '__main__':
    window()

# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 500, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a QDateEdit widget
        date = QDateEdit(self)

        # setting geometry of the date edit
        date.setGeometry(100, 100, 150, 40)

        # creating a label
        label = QLabel("GeeksforGeeks", self)

        # setting geometry
        label.setGeometry(100, 150, 200, 60)

        # making label multiline
        label.setWordWrap(True)

        # date  change signal
        date.dateChanged.connect(lambda: method())

        # method called when signal emitted
        def method():
            # setting text to the label
            label.setText("Date  Changed Signal")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.browse.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.png, *.xmp *.jpg)')
        self.filename.setText(fname[0])

app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_() 

from datetime import datetime, timedelta

if __name__ == '__main__':
    today = datetime.now()
    yesterday = today - timedelta(1)
    daybefore = today - timedelta(2)
    print(today.strftime("%d-%m-%Y"), yesterday.strftime("%d-%m-%Y"), daybefore.strftime("%d-%m-%Y"))

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QCompleter
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(740, 500)

        # fnt = QFont('Open Sans', 12)

        mainLayout = QVBoxLayout()

        # input field
        self.input = QLineEdit()
        # self.input.setFixedHeight(50)
        # self.input.setFont(fnt)
        self.input.editingFinished.connect(self.addEntry)


        mainLayout.addWidget(self.input)

        self.model = QStandardItemModel()
        completer = QCompleter(self.model, self)
        self.input.setCompleter(completer)

        self.init()

        self.console = QTextEdit()
        # self.console.setFont(fnt)

        mainLayout.addWidget(self.console)
        self.setLayout(mainLayout)

    def addEntry(self):
        print("Hola Mundo")
        # entryItem = self.input.text()
        # self.input.clear()
        # self.console.append(entryItem)

        # if not self.model.findItems(entryItem):
        #     self.model.appendRow(QStandardItem(entryItem))

    def init(self):
        obj1 = user("Ivan", "993324631")
        txt_1 = "993324631"
        obj2 = user("Miguel", "962623258")
        txt_2= "962623258"
        txt_3= "940184094"
        self.model.appendRow(QStandardItem(txt_1))
        self.model.appendRow(QStandardItem(txt_2))
        self.model.appendRow(QStandardItem(txt_3))



class user:
    def __init__(self, name, telf):
        self.name = name
        self.telf = telf


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
"""

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QComboBox, QVBoxLayout
#
# class comboCompanies(QComboBox):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setStyleSheet('font-size: 20px')
#         self.addItems(['Pendiente', 'Consignacion', 'Contado', 'Credito'])
#         self.setEditable(True)
#         self.setCurrentIndex(-1)
#         self.lineEdit().setPlaceholderText("Tipo")
#         # self.setCurrentText("Pendiente")
#         # self.setPlaceholderText("Ivan")
#     #     self.currentIndexChanged.connect(self.getComboValue)
#     #
#     # def getComboValue(self):
#     #     print(self.currentText())
#     #     # return self.currentText()
#
# class TableWidget(QTableWidget):
#     def __init__(self):
#         super().__init__(1, 5)
#         self.setHorizontalHeaderLabels(list('ABCDE'))
#         self.setColumnWidth(4, 100)
#         self.verticalHeader().setDefaultSectionSize(40)
#         self.horizontalHeader().setDefaultSectionSize(150)
#
#         combo = comboCompanies(self)
#         combo_ = comboCompanies(self)
#         self.setCellWidget(0, 4, combo)
#         self.setCellWidget(0, 3, combo_)
#
# class AppDemo(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.resize(1000, 600)
#
#         mainLayout = QVBoxLayout()
#         table = TableWidget()
#         mainLayout.addWidget(table)
#
#         self.setLayout(mainLayout)
#
# app = QApplication(sys.argv)
# demo = AppDemo()
# demo.show()
# app.exit(app.exec_())
#

# from fpdf import FPDF
#
# class PDF(FPDF):
#     def titles(self, title):
#         self.set_xy(5.0,23.0)
#         self.set_font('Arial', 'BU', 14)
#         self.set_text_color(0, 0, 0)
#         self.cell(w=70.0, h=5.0, align='C', txt=title, border=0)
#
#     def addImage(self, name, x, y, w, h):
#         self.image(name, x, y, w, h)
#
# if __name__ == "__main__":
#     pdf = PDF('P', 'mm', format = (80.0, 100.0))
#     pdf.add_page()
#     pdf.addImage("C:/Users/IROJAS/PycharmProjects/genesis/logo_genesis.png", 25.75, 7, 28.5, 12)
#     pdf.titles("Reporte Proveedor")
#     # pdf.set_author("Ivan Rojas Carrasco")
#     pdf.output("Prueba.pdf", "F")
#
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5 import QtGui
# import sys
#
# class Validator(QtGui.QValidator):
#     def validate(self, string, pos):
#         return QtGui.QValidator.Acceptable, string.upper(), pos
#
#
# def keyPressEvent(e):
#     # print("Hola Mundo")
#     pass
#     # if e.key() == Qt.Key_Enter:
#     #     print("enter")
#
#
#
# class main_(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):  # para que puse el parent = None?
#         super(main_, self).__init__(parent)
#
#         self.setObjectName("LoginWindow")
#         self.resize(380, 312)
#         self.setFixedSize(380,312)
#         # self.centralwidget = QtWidgets.QWidget(LoginWindow)
#         # self.centralwidget.setObjectName("centralwidget")
#
#         self.txtLabel = QtWidgets.QLabel(self)
#         self.txtLabel.setText("Hola Mundo")
#         self.txtLabel.setGeometry(QtCore.QRect(70, 80, 150, 20))
#
#
#         self.edit = QtWidgets.QLineEdit(self)
#         self.edit.setGeometry(QtCore.QRect(70, 170, 230, 20))
#         self.strList = ["GERMANY", "SPAIN", "FRANCE", "NORWAY"]
#         self.completer = QCompleter(self.strList, self.edit)
#         self.completer.setFilterMode(Qt.MatchContains)
#         self.completer.setCompletionMode(QCompleter.PopupCompletion)
#         # self.completer.setCaseSensitivity(Qt.CaseInsensitive)
#         # self.completer.popup().installEventFilter(self)
#         # self.completer.popup().mouseReleaseEvent = self.ivan
#         # self.completer.mouseReleaseEvent = self.ivan
#         self.completer.activated.connect(self.hola)
#         self.validator = Validator()
#         self.edit.setValidator(self.validator)
#         self.edit.setCompleter(self.completer)
#         # self.edit.returnPressed.connect(self.hola)
#         # self.edit.mouseReleaseEvent = self.ivan
#         # self.edit.installEventFilter(self)
#         self.edit.setClearButtonEnabled(True)

    # def ivan(self, event):
    #     print("Hola Mundo")

    # def eventFilter(self, obj, event):
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         if event.button() == QtCore.Qt.LeftButton:
    #             print(obj.objectName(), "Left click")
    #         # elif event.button() == QtCore.Qt.RightButton:
    #         #     print(obj.objectName(), "Right click")
    #         # elif event.button() == QtCore.Qt.MiddleButton:
    #         #     print(obj.objectName(), "Middle click")
    #     return QtCore.QObject.event(obj, event)

#
#     def hola(self):
#         self.txtLabel.setText(self.edit.text())
#         # print(self.edit.text())
#
#
# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     # LoginWindow = QtWidgets.QMainWindow()
#     ui = main_()
#     # ui.setupUi(LoginWindow)
#     ui.show()
#     app.exec_()

# importing libraries
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# import sys
# import time
#
#
# class Example(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         # calling initUI method
#         self.initUI()
#
#     # method for creating widgets
#     def initUI(self):
#
#         self.cant = 0
#         # creating progress bar
#         self.pbar = QProgressBar(self)
#
#         # setting its geometry
#         self.pbar.setGeometry(30, 40, 200, 25)
#
#         # creating push button
#         self.btn = QPushButton('Start', self)
#
#         # changing its position
#         self.btn.move(40, 80)
#
#         # adding action to push button
#         self.btn.clicked.connect(self.doAction)
#
#         # setting window geometry
#         self.setGeometry(300, 300, 280, 170)
#
#         # setting window action
#         self.setWindowTitle("Python")
#
#         # showing all the widgets
#         self.show()
#
#     # when button is pressed this method is being called
#     def doAction(self):
#         # setting for loop to set value of progress bar
#         self.cant += 5
#         self.pbar.setValue(self.cant)
#         # for i in range(101):
#         #     # slowing down the loop
#         #     time.sleep(0.1)
#         #
#         #     # setting value to progress bar
#         #     self.pbar.setValue(i)
#
#
# # main method
# if __name__ == '__main__':
#     # create pyqt5 app
#     App = QApplication(sys.argv)
#
#     # create the instance of our Window
#     window = Example()
#
#     # start the app
#     sys.exit(App.exec())

from PyQt5 import QtCore, QtWidgets
import numpy as np

class HorizontalHeader(QtWidgets.QHeaderView):
    def __init__(self, values, parent=None):
        super(HorizontalHeader, self).__init__(QtCore.Qt.Horizontal, parent)
        self.setSectionsMovable(True)
        self.comboboxes = []
        self.sectionResized.connect(self.handleSectionResized)
        self.sectionMoved.connect(self.handleSectionMoved)

    def showEvent(self, event):
        for i in range(self.count()):
            if i < len(self.comboboxes):
                combo = self.comboboxes[i]
                combo.clear()
                combo.addItems(["Variable", "Timestamp"])
            else:
                combo = QtWidgets.QComboBox(self)
                combo.addItems(["Variable", "Timestamp"])
                self.comboboxes.append(combo)

            combo.setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i)-4, self.height())
            combo.show()

        if len(self.comboboxes) > self.count():
            for i in range(self.count(), len(self.comboboxes)):
                self.comboboxes[i].deleteLater()

        super(HorizontalHeader, self).showEvent(event)

    def handleSectionResized(self, i):
        for i in range(self.count()):
            j = self.visualIndex(i)
            logical = self.logicalIndex(j)
            self.comboboxes[i].setGeometry(self.sectionViewportPosition(logical), 0, self.sectionSize(logical)-4, self.height())

    def handleSectionMoved(self, i, oldVisualIndex, newVisualIndex):
        for i in range(min(oldVisualIndex, newVisualIndex), self.count()):
            logical = self.logicalIndex(i)
            self.comboboxes[i].setGeometry(self.ectionViewportPosition(logical), 0, self.sectionSize(logical) - 5, height())

    def fixComboPositions(self):
        for i in range(self.count()):
            self.comboboxes[i].setGeometry(self.sectionViewportPosition(i), 0, self.sectionSize(i) - 5, self.height())

class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        header = HorizontalHeader(self)
        self.setHorizontalHeader(header)

    def scrollContentsBy(self, dx, dy):
        super(TableWidget, self).scrollContentsBy(dx, dy)
        if dx != 0:
            self.horizontalHeader().fixComboPositions()

class App(QtWidgets.QWidget):
    def __init__(self):
        super(App,self).__init__()
        self.data = np.random.rand(10, 10)
        self.createTable()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        self.showMaximized()

    def createTable(self):
        self.header = []
        self.table = TableWidget(*self.data.shape)
        for i, row_values in enumerate(self.data):
            for j, value in enumerate(row_values):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))
        self.table.verticalHeader().hide()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


