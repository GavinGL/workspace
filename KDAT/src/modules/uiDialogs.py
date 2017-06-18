# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\Dialogsui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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

class Ui_DialogLinks(object):
    def setupUi(self, DialogLinks):
        DialogLinks.setObjectName(_fromUtf8("DialogLinks"))
        DialogLinks.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogLinks.resize(344, 300)
        self.pushButton_Connect = QtGui.QPushButton(DialogLinks)
        self.pushButton_Connect.setGeometry(QtCore.QRect(250, 172, 75, 23))
        self.pushButton_Connect.setObjectName(_fromUtf8("pushButton_Connect"))
        self.pushButton_Cancel = QtGui.QPushButton(DialogLinks)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.listWidget_DialogList = QtGui.QListWidget(DialogLinks)
        self.listWidget_DialogList.setGeometry(QtCore.QRect(20, 40, 201, 221))
        self.listWidget_DialogList.setObjectName(_fromUtf8("listWidget_DialogList"))
        self.pushButton_Change = QtGui.QPushButton(DialogLinks)
        self.pushButton_Change.setGeometry(QtCore.QRect(250, 106, 75, 23))
        self.pushButton_Change.setObjectName(_fromUtf8("pushButton_Change"))
        self.label = QtGui.QLabel(DialogLinks)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_ReNew = QtGui.QPushButton(DialogLinks)
        self.pushButton_ReNew.setGeometry(QtCore.QRect(250, 40, 75, 23))
        self.pushButton_ReNew.setObjectName(_fromUtf8("pushButton_ReNew"))

        self.retranslateUi(DialogLinks)
        self.listWidget_DialogList.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(DialogLinks)
        DialogLinks.setTabOrder(self.listWidget_DialogList, self.pushButton_Change)
        DialogLinks.setTabOrder(self.pushButton_Change, self.pushButton_Connect)
        DialogLinks.setTabOrder(self.pushButton_Connect, self.pushButton_Cancel)

    def retranslateUi(self, DialogLinks):
        DialogLinks.setWindowTitle(_translate("DialogLinks", "所有会话", None))
        self.pushButton_Connect.setText(_translate("DialogLinks", "连接", None))
        self.pushButton_Cancel.setText(_translate("DialogLinks", "取消", None))
        self.pushButton_Change.setText(_translate("DialogLinks", "修改", None))
        self.label.setText(_translate("DialogLinks", "会话列表", None))
        self.pushButton_ReNew.setText(_translate("DialogLinks", "刷新", None))

