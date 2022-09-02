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
    window() """

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