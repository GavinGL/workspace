# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\Emailui.ui'
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

class Ui_DialogEmail(object):
    def setupUi(self, DialogEmail):
        DialogEmail.setObjectName(_fromUtf8("DialogEmail"))
        DialogEmail.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogEmail.resize(342, 335)
        self.textEdit_Recipients = QtGui.QTextEdit(DialogEmail)
        self.textEdit_Recipients.setGeometry(QtCore.QRect(90, 77, 201, 81))
        self.textEdit_Recipients.setObjectName(_fromUtf8("textEdit_Recipients"))
        self.pushButton_EmailSend = QtGui.QPushButton(DialogEmail)
        self.pushButton_EmailSend.setGeometry(QtCore.QRect(80, 290, 75, 23))
        self.pushButton_EmailSend.setObjectName(_fromUtf8("pushButton_EmailSend"))
        self.pushButton_EmailCancel = QtGui.QPushButton(DialogEmail)
        self.pushButton_EmailCancel.setGeometry(QtCore.QRect(200, 290, 75, 23))
        self.pushButton_EmailCancel.setObjectName(_fromUtf8("pushButton_EmailCancel"))
        self.lineEdit_Sender = QtGui.QLineEdit(DialogEmail)
        self.lineEdit_Sender.setGeometry(QtCore.QRect(90, 37, 201, 20))
        self.lineEdit_Sender.setObjectName(_fromUtf8("lineEdit_Sender"))
        self.label = QtGui.QLabel(DialogEmail)
        self.label.setGeometry(QtCore.QRect(30, 35, 54, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogEmail)
        self.label_2.setGeometry(QtCore.QRect(30, 78, 54, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(DialogEmail)
        self.label_3.setGeometry(QtCore.QRect(30, 178, 54, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.textEdit_CC = QtGui.QTextEdit(DialogEmail)
        self.textEdit_CC.setGeometry(QtCore.QRect(90, 178, 201, 81))
        self.textEdit_CC.setObjectName(_fromUtf8("textEdit_CC"))

        self.retranslateUi(DialogEmail)
        QtCore.QMetaObject.connectSlotsByName(DialogEmail)
        DialogEmail.setTabOrder(self.lineEdit_Sender, self.textEdit_Recipients)
        DialogEmail.setTabOrder(self.textEdit_Recipients, self.textEdit_CC)
        DialogEmail.setTabOrder(self.textEdit_CC, self.pushButton_EmailSend)
        DialogEmail.setTabOrder(self.pushButton_EmailSend, self.pushButton_EmailCancel)

    def retranslateUi(self, DialogEmail):
        DialogEmail.setWindowTitle(_translate("DialogEmail", "发送报告", None))
        self.textEdit_Recipients.setHtml(_translate("DialogEmail", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">输入新增收件人邮箱，以“；”隔开……</span></p></body></html>", None))
        self.pushButton_EmailSend.setText(_translate("DialogEmail", "发送", None))
        self.pushButton_EmailCancel.setText(_translate("DialogEmail", "取消", None))
        self.label.setText(_translate("DialogEmail", "发件人：", None))
        self.label_2.setText(_translate("DialogEmail", "收件人：", None))
        self.label_3.setText(_translate("DialogEmail", "抄送：", None))
        self.textEdit_CC.setHtml(_translate("DialogEmail", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">输入新增抄送人邮箱，以“；”隔开……</span></p></body></html>", None))

