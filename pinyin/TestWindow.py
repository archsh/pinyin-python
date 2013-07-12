# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestWindow.ui'
#
# Created: Sun Jul 14 14:55:10 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!
import sys,os
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
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lineEdit_Pinyin = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Pinyin.setText(_fromUtf8(""))
        self.lineEdit_Pinyin.setObjectName(_fromUtf8("lineEdit_Pinyin"))
        self.horizontalLayout_3.addWidget(self.lineEdit_Pinyin)
        self.pushButton_Clear = QtGui.QPushButton(self.groupBox)
        self.pushButton_Clear.setObjectName(_fromUtf8("pushButton_Clear"))
        self.horizontalLayout_3.addWidget(self.pushButton_Clear)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_Pinyins = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Pinyins.setObjectName(_fromUtf8("groupBox_Pinyins"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_Pinyins)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_Pinyins = QtGui.QLineEdit(self.groupBox_Pinyins)
        self.lineEdit_Pinyins.setObjectName(_fromUtf8("lineEdit_Pinyins"))
        self.horizontalLayout_2.addWidget(self.lineEdit_Pinyins)
        self.verticalLayout_2.addWidget(self.groupBox_Pinyins)
        self.groupBox_Words = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Words.setObjectName(_fromUtf8("groupBox_Words"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_Words)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit_Words = QtGui.QPlainTextEdit(self.groupBox_Words)
        self.plainTextEdit_Words.setReadOnly(True)
        self.plainTextEdit_Words.setPlainText(_fromUtf8(""))
        self.plainTextEdit_Words.setObjectName(_fromUtf8("plainTextEdit_Words"))
        self.verticalLayout.addWidget(self.plainTextEdit_Words)
        self.verticalLayout_2.addWidget(self.groupBox_Words)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lineEdit_Pinyin, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pinyin_query)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit_Pinyin.clear)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.lineEdit_Pinyins.clear)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.plainTextEdit_Words.clear)
        QtCore.QObject.connect(self.lineEdit_Pinyins, QtCore.SIGNAL(_fromUtf8("cursorPositionChanged(int,int)")), self.pinyin_select)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Clear.setText(_translate("MainWindow", "Clear", None))
        self.groupBox_Pinyins.setTitle(_translate("MainWindow", "Pinyin(s)", None))
        self.groupBox_Words.setTitle(_translate("MainWindow", "Filtered Words", None))
    
    
    def pinyin_select(self, pos1,pos2):
        #print 'pos1:%d, pos2: %d'%(pos1,pos2)
        if self._py and self._pys:
            pos = 0
            idx = 0
            for w in self._pys:
                if pos2>= pos and pos2<= pos+len(w):
                    words = self.pyinst.query(self._py,index=idx)
                    self.plainTextEdit_Words.setPlainText('\n'.join(words))
                    #('\n'.join(self.pyinst.pinyin_split(py)))
                    self.groupBox_Words.setTitle("Filtered Words: %d"%len(words))
                pos += len(w)+1
                idx += 1
            
    
    def pinyin_query(self, py):
        py = str(py)
        if py:
            pys   = self.pyinst.pinyin_split(py)
            words = self.pyinst.query(py,index=len(pys)-1)
            self._py = py
            self._pys = pys
            self.lineEdit_Pinyins.setText(" ".join(pys))
            self.plainTextEdit_Words.setPlainText('\n'.join(words))
            #('\n'.join(self.pyinst.pinyin_split(py)))
            self.groupBox_Words.setTitle("Filtered Words: %d"%len(words))
        else:
            self._py = None
            self._pys = None
            self.plainTextEdit_Words.setPlainText('')
            self.lineEdit_Pinyins.setText("")
            self.groupBox_Words.setTitle("Filtered Words")
    


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

