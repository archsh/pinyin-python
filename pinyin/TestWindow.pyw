# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestWindow.ui'
#
# Created: Sun Jul 14 14:55:10 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!
import sys,os
sys.path.append('../pinyin')
import datetime
import pinyin
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.pyinst = pinyin.Pinyin()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(559, 606)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft Sans Serif"))
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_Pinyin = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_Pinyin.setText(_fromUtf8(""))
        self.lineEdit_Pinyin.setObjectName(_fromUtf8("lineEdit_Pinyin"))
        self.horizontalLayout.addWidget(self.lineEdit_Pinyin)
        self.pushButton_Clear = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Clear.setObjectName(_fromUtf8("pushButton_Clear"))
        self.horizontalLayout.addWidget(self.pushButton_Clear)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit_Words = QtGui.QPlainTextEdit(self.groupBox)
        self.plainTextEdit_Words.setReadOnly(True)
        self.plainTextEdit_Words.setPlainText(_fromUtf8(""))
        self.plainTextEdit_Words.setObjectName(_fromUtf8("plainTextEdit_Words"))
        self.verticalLayout.addWidget(self.plainTextEdit_Words)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit_Pinyin.clear)
        QtCore.QObject.connect(self.lineEdit_Pinyin, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pinyin_query)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.plainTextEdit_Words.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Clear.setText(_translate("MainWindow", "Clear", None))
        self.groupBox.setTitle(_translate("MainWindow", "Filtered Words", None))
    
    def pinyin_query(self, pinyin):
        self.plainTextEdit_Words.setPlainText('\n'.join(self.pyinst.pinyin_split(pinyin)))
    


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

