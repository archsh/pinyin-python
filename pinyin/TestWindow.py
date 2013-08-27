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
        t1 = datetime.datetime.now()
        self.pyinst = pinyin.Pinyin()
        t2 = datetime.datetime.now()
        self.pyinst.load_phrases(filename='../datas/phrase.json')
        t3 = datetime.datetime.now()
        print 't2-t1:',t2-t1
        print 't3-t2:',t3-t2
        self._py=None
        self._pys=None
        self._words=None
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
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lineEdit_Inputed = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_Inputed.setReadOnly(True)
        self.lineEdit_Inputed.setObjectName(_fromUtf8("lineEdit_Inputed"))
        self.verticalLayout_3.addWidget(self.lineEdit_Inputed)
        self.verticalLayout_2.addWidget(self.groupBox_2)
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
        self.label_Timespent = QtGui.QLabel(self.groupBox_Pinyins)
        self.label_Timespent.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_Timespent.setFont(font)
        self.label_Timespent.setText(_fromUtf8(""))
        self.label_Timespent.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_Timespent.setObjectName(_fromUtf8("label_Timespent"))
        self.horizontalLayout_2.addWidget(self.label_Timespent)
        self.verticalLayout_2.addWidget(self.groupBox_Pinyins)
        self.groupBox_Words = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_Words.setObjectName(_fromUtf8("groupBox_Words"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_Words)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget_Words = QtGui.QListWidget(self.groupBox_Words)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_Words.setFont(font)
        self.listWidget_Words.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget_Words.setProperty("showDropIndicator", False)
        self.listWidget_Words.setResizeMode(QtGui.QListView.Adjust)
        self.listWidget_Words.setLayoutMode(QtGui.QListView.Batched)
        self.listWidget_Words.setSpacing(3)
        self.listWidget_Words.setGridSize(QtCore.QSize(20, 20))
        #self.listWidget_Words.setViewMode(QtGui.QListView.IconMode)
        self.listWidget_Words.setUniformItemSizes(True)
        self.listWidget_Words.setWordWrap(True)
        self.listWidget_Words.setObjectName(_fromUtf8("listWidget_Words"))
        self.verticalLayout.addWidget(self.listWidget_Words)
        self.verticalLayout_2.addWidget(self.groupBox_Words)
        MainWindow.setCentralWidget(self.centralwidget)
        self.lineEdit_Pinyin.setFocus()

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lineEdit_Pinyin, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pinyin_query)
        QtCore.QObject.connect(self.pushButton_Clear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clear_pinyin_all)
        QtCore.QObject.connect(self.lineEdit_Pinyins, QtCore.SIGNAL(_fromUtf8("cursorPositionChanged(int,int)")), self.pinyin_select)
        QtCore.QObject.connect(self.listWidget_Words, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), self.words_selected)
        #QtCore.QObject.connect(MainWindow, QtCore.SIGNAL(_fromUtf8("close()")), self.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #MainWindow.close = self.close

    def update_json(self):
        print 'Closing ...'
        self.pyinst.save_dictionary('my_dictionary.json')
        self.pyinst.save_phrases('my_phrases.json')
        return True
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Clear.setText(_translate("MainWindow", "Clear", None))
        self.groupBox_Pinyins.setTitle(_translate("MainWindow", "Pinyin(s)", None))
        self.groupBox_Words.setTitle(_translate("MainWindow", "Filtered Words", None))
    
    def clear_pinyin_all(self):
        self.lineEdit_Pinyin.clear()
        self.lineEdit_Pinyins.clear()
        self.listWidget_Words.clear()
        self._py  = None
        self._pys = None
        self._words = None
        self.update_json()
    
    
    def words_selected(self, item):
        if not self._py or not self._pys:
            return
        self._words = self._words+unicode(item.text()) if self._words else unicode(item.text())
        print 'Selected Words:',self._words
        self.lineEdit_Inputed.setText(self._words)
        if len(self._words)>= len(self._pys):
            self.listWidget_Words.clear()
            print 'Pys:','-'.join(self._pys),self._words
            self.pyinst.report(self._pys,self._words)
        else:
            t1 = datetime.datetime.now()
            pys, words = self.pyinst.query(self._py,index=len(self._words),selected=self._words)
            t2 = datetime.datetime.now()
            self.label_Timespent.setText("%s"%(t2-t1))
            self.listWidget_Words.clear()
            self.listWidget_Words.addItems(words)
            self.groupBox_Words.setTitle("Filtered Words: %d"%len(words))
    
    def pinyin_select(self, pos1,pos2):
        #print 'pos1:%d, pos2: %d'%(pos1,pos2)
        if self._py and self._pys:
            pos = 0
            idx = 0
            for w in self._pys:
                if pos2>= pos and pos2<= pos+len(w):
                    t1 = datetime.datetime.now()
                    pys, words = self.pyinst.query(self._py,index=idx)
                    t2 = datetime.datetime.now()
                    self.label_Timespent.setText("%s"%(t2-t1))
                    self.listWidget_Words.clear()
                    self.listWidget_Words.addItems(words)
                    self.groupBox_Words.setTitle("Filtered Words: %d"%len(words))
                pos += len(w)+1
                idx += 1
            
    
    def pinyin_query(self, py):
        py = str(py)
        self._words = None
        self.lineEdit_Inputed.setText('')
        if py:
            t1 = datetime.datetime.now()
            pys, words = self.pyinst.query(py)
            t2 = datetime.datetime.now()
            self._py = py
            self._pys = pys
            self.label_Timespent.setText("%s"%(t2-t1))
            self.lineEdit_Pinyins.setText(" ".join(pys))
            self.listWidget_Words.clear()
            self.listWidget_Words.addItems(words)
            self.groupBox_Words.setTitle("Filtered Words: %d"%len(words))
        else:
            self._py = None
            self._pys = None
            self.listWidget_Words.clear()
            #self.listWidget_Words.addItems(words)
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

