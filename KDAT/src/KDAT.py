# -*- coding: UTF-8 -*-

import os
import sys
import ConfigParser
import socket
import string
import threading,time,paramiko

from PyQt4 import QtGui,QtCore
from modules.uiKDAT import Ui_MainWindow
from modules.uiConnect import Ui_DialogConnect
from modules.uiDialogs import Ui_DialogLinks
from modules.uiEmail import Ui_DialogEmail
from modules.myClass import *
from modules.myConnect import myConnect
from system.GetHardwareInfo import GetHardInfo
from system.GetSoftwareInfo import GetSoftInfo
from system.GetEepromInfo import GetEepromInfo

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
'''
主程序窗口
'''
class myWindow(QtGui.QMainWindow,Ui_MainWindow):  
	def __init__(self,parent=None):  
		super(myWindow,self).__init__(parent)
		self.setupUi(self)

		##########################
		######  初始化参数  ######
		##########################
		self.allInit()

		self.CreatDir()

		##########################
		###  【菜单】控件设置  ###
		##########################

		#单击【帮助-关于KDAT】，弹出信息窗口
		self.connect(self.action_About, QtCore.SIGNAL('triggered()'), self.About)

		#单击【连接-新建】，弹出连接窗口
		self.diaConnect = myDiaConnect()
		self.connect(self.action_New, QtCore.SIGNAL('triggered()'), self.diaConnect.show)

		#单击【连接-打开】，弹出所有会话窗口
		self.diaLinks = myDialogLinks()
		self.connect(self.action_Open, QtCore.SIGNAL('triggered()'), self.diaLinks.show)

		#单击【连接-断开】，断开连接
		self.connect(self.action_Break,QtCore.SIGNAL('triggered()'),self.myLinkBreak)

		#单击【连接-退出】，关闭程序
		self.connect(self.action_Exit,QtCore.SIGNAL('triggered()'),QtGui.qApp, QtCore.SLOT('quit()'))

		##########################
		###  【主页】控件设置  ###
		##########################

		#单击【Start】按钮，开始分析
		self.connect(self.pushButton_StartAll, QtCore.SIGNAL('clicked()'), self.myStartAll)

		#单击【发送报告】按钮，开始邮件发送配置
		self.sendEmail = myEmail()
		self.connect(self.pushButton_Email, QtCore.SIGNAL('clicked()'), self.sendEmail.show)

		self.statusBar().showMessage(_fromUtf8('等待配置完成...'))

		#模式选择设置
		self.connect(self.radioButton_OneKey, QtCore.SIGNAL('clicked()'), self.pushOneKeyButton)
		self.connect(self.radioButton_Custom, QtCore.SIGNAL('clicked()'), self.pushCustomButton)

		##########################
		## 【系统分析】控件设置 ##
		##########################

		#复选框选择
		self.connect(self.checkBox_SysAll, QtCore.SIGNAL('clicked()'), self.checkSysAllSet)
		self.connect(self.checkBox_SysE2prom, QtCore.SIGNAL('clicked()'), self.checkSysE2promSet)
		self.connect(self.checkBox_SysHardware, QtCore.SIGNAL('clicked()'), self.checkSysHardware)
		self.connect(self.checkBox_SysSoftware, QtCore.SIGNAL('clicked()'), self.checkSysSoftware)

		#保存参数按钮
		self.connect(self.pushButton_SysSave, QtCore.SIGNAL('clicked()'), self.pushButtonSysSave)

		#开始分析按钮
		self.connect(self.pushButton_SysStart, QtCore.SIGNAL('clicked()'), self.pushButtonSysStart)

		##########################
		## 【运行状态】控件设置 ##
		##########################

		##########################
		## 【网络分析】控件设置 ##
		##########################

		##########################
		## 【媒体分析】控件设置 ##
		##########################

		##########################
		## 【高级分析】控件设置 ##
		##########################

		##########################
		## 【业务分析】控件设置 ##
		##########################

	def myInit(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')

		self.progressBar_Home.setValue(0)
		self.progressBar_Sys.setValue(0)
		self.progressBar_Run.setValue(0)
		self.progressBar_Net.setValue(0)
		self.progressBar_Media.setValue(0)
		self.progressBar_Advanced.setValue(0)
		self.progressBar_App.setValue(0)

		cp_link.set('myconfig','currentstep','0')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','allstep','0')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

	def allInit(self):
		f=open(os.getcwd()+'/env.conf','w')
		f.write('[myconfig]')
		f.close()

		self.myInit()

		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')

		cp_link.set('myconfig','reportdir',str(os.getcwd()+'\\KDATReport\\'))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','linkstatus','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','checksysall','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','checksyse2prom','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','checksyshardware','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','checksyssoftware','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		cp_link.set('myconfig','openstatus','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

	def myLinkBreak(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','linkstatus','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('当前会话已断开'))

	def pushButtonSysStart(self):
		self.statusBar().showMessage(_fromUtf8('暂未实现...'))

	def pushButtonSysSave(self):
		self.statusBar().showMessage(_fromUtf8('当前页配置保存完成...'))

	def checksys(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		if self.checkBox_SysE2prom.isChecked():
			cp_link.set('myconfig','checksyse2prom','True')
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
			if self.checkBox_SysHardware.isChecked():
				cp_link.set('myconfig','checksyshardware','True')
				cp_link.write(open(os.getcwd()+'/env.conf','w'))
				if self.checkBox_SysSoftware.isChecked():
					cp_link.set('myconfig','checksyssoftware','True')
					cp_link.write(open(os.getcwd()+'/env.conf','w'))
					self.checkBox_SysAll.setChecked(True)
					cp_link.set('myconfig','checksysall',str(self.checkBox_SysAll.isChecked()))
					cp_link.write(open(os.getcwd()+'/env.conf','w'))
				else:
					cp_link.set('myconfig','checksyssoftware','False')
					cp_link.write(open(os.getcwd()+'/env.conf','w'))
					self.checkBox_SysAll.setChecked(False)
					cp_link.set('myconfig','checksysall',str(self.checkBox_SysAll.isChecked()))
					cp_link.write(open(os.getcwd()+'/env.conf','w'))
			else:
				cp_link.set('myconfig','checksyshardware','False')
				cp_link.write(open(os.getcwd()+'/env.conf','w'))
				self.checkBox_SysAll.setChecked(False)
				cp_link.set('myconfig','checksysall',str(self.checkBox_SysAll.isChecked()))
				cp_link.write(open(os.getcwd()+'/env.conf','w'))
		else:
			cp_link.set('myconfig','checksyse2prom','False')
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
			self.checkBox_SysAll.setChecked(False)
			cp_link.set('myconfig','checksysall',str(self.checkBox_SysAll.isChecked()))
			cp_link.write(open(os.getcwd()+'/env.conf','w'))

		if self.checkBox_SysAll.isChecked() is False:
			self.radioButton_OneKey.setChecked(False)
			self.radioButton_Custom.setChecked(True)
			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			cp_link.set('myconfig','debugmode','custom')
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
		else:
			self.radioButton_OneKey.setChecked(True)
			self.radioButton_Custom.setChecked(False)
			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			cp_link.set('myconfig','debugmode','onekey')
			cp_link.write(open(os.getcwd()+'/env.conf','w'))

	def checkSysSoftware(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','checksyssoftware',str(self.checkBox_SysSoftware.isChecked()))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		self.checksys()

	def checkSysHardware(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','checksyshardware',str(self.checkBox_SysHardware.isChecked()))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		self.checksys()

	def checkSysE2promSet(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','checksyse2prom',str(self.checkBox_SysE2prom.isChecked()))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		self.checksys()

	def checkSysAllSet(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','checksysall',str(self.checkBox_SysAll.isChecked()))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		if self.checkBox_SysAll.isChecked():
			self.checkBox_SysE2prom.setChecked(True)
			self.checkSysE2promSet()
			self.checkBox_SysHardware.setChecked(True)
			self.checkSysHardware()
			self.checkBox_SysSoftware.setChecked(True)
			self.checkSysSoftware()
		else:
			self.checkBox_SysE2prom.setChecked(False)
			self.checkSysE2promSet()
			self.checkBox_SysHardware.setChecked(False)
			self.checkSysHardware()
			self.checkBox_SysSoftware.setChecked(False)
			self.checkSysSoftware()

	def CreatDir(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		homedir = cp_link.get('myconfig','reportdir')
		if (os.path.exists(homedir+'/log/systemlog') == False ):
			os.makedirs(homedir+'/log/systemlog')
		if (os.path.exists(homedir+'/log/toollog') == False ):
			os.makedirs(homedir+'/log/toollog')
		if (os.path.exists(homedir+'/log/advancelog') == False ):
			os.makedirs(homedir+'/log/advancelog')
		if (os.path.exists(homedir+'/log/applog') == False ):
			os.makedirs(homedir+'/log/applog')
		if (os.path.exists(homedir+'/log/medialog') == False ):
			os.makedirs(homedir+'/log/medialog')
		if (os.path.exists(homedir+'/log/networklog') == False ):
			os.makedirs(homedir+'/log/networklog')
		if (os.path.exists(homedir+'/log/runninglog') == False ):
			os.makedirs(homedir+'/log/runninglog')
		if (os.path.exists(homedir+'dialogs') == False ):
			os.makedirs(homedir+'dialogs')

	def stepCount(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		allstep = cp_link.getint('myconfig','allstep')
		self.progressBar_Home.setMinimum(0)
		self.progressBar_Home.setMaximum(allstep)

		while True:
			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			if cp_link.getint('myconfig','currentstep') < allstep:
				self.progressBar_Home.setValue(cp_link.getint('myconfig','currentstep'))
				time.sleep(.1)
			else:
				self.progressBar_Home.setValue(cp_link.getint('myconfig','currentstep'))
				break

	def About(self):
		QtGui.QMessageBox.question(self,_fromUtf8('关于KDAT'),_fromUtf8('Kedacom Debug & Analysis Tool （V1.0）\
			Copyright(c)Suzhou Keda Technology Co.,Ltd All rights reserved.\r\n'),QtGui.QMessageBox.Ok)

	def pushOneKeyButton(self):
		self.statusBar().showMessage(_fromUtf8('已选【一键分析】，点击【Start】按钮开始分析！！！'))
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','debugmode','onekey')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		self.checkBox_SysE2prom.setChecked(True)
		self.checkSysE2promSet()
		self.checkBox_SysHardware.setChecked(True)
		self.checkSysHardware()
		self.checkBox_SysSoftware.setChecked(True)
		self.checkSysSoftware()

	def pushCustomButton(self):
		self.statusBar().showMessage(_fromUtf8('已选【自定义分析】，请开始进行配置...'))
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','debugmode','custom')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

	#【Start】按钮实现
	def myStartAll(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','currentstep','0')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		
		cp_link.set('myconfig','allstep','0')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

		if cp_link.getboolean('myconfig','linkstatus'):
			self.statusBar().showMessage(_fromUtf8('连接已建立...'))
			#try:
			for case in switch(cp_link.get('myconfig','debugmode')):
				if case ('onekey'):
					self.statusBar().showMessage(_fromUtf8('开始一键分析...'))
					self.myProcess()
					break
				if case ('custom'):
					self.statusBar().showMessage(_fromUtf8('开始自定义分析...'))
					self.myProcess()
					break
				if case():
					self.statusBar().showMessage(_fromUtf8('参数异常...'))
					QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('参数异常'),
						QtGui.QMessageBox.Ok)
					break
			"""
			except:
				print cp_link.get('myconfig','debugmode')
				self.statusBar().showMessage(_fromUtf8('分析模式未设置...'))
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('请选择模式'),
						QtGui.QMessageBox.Ok)
			"""
		else:
			self.statusBar().showMessage(_fromUtf8('未建立连接...'))
			QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('未建立连接，请重新连接！'),
						QtGui.QMessageBox.Ok)
		self.myInit()

	def myProcess(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		if cp_link.getboolean('myconfig','checksyse2prom'):
			cp_link.set('myconfig','allstep',str(cp_link.getint('myconfig','allstep')+2))
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
		if cp_link.getboolean('myconfig','checksyshardware'):
			cp_link.set('myconfig','allstep',str(cp_link.getint('myconfig','allstep')+8))
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
		if cp_link.getboolean('myconfig','checksyssoftware'):
			cp_link.set('myconfig','allstep',str(cp_link.getint('myconfig','allstep')+0))
			cp_link.write(open(os.getcwd()+'/env.conf','w'))

		threads = []
		t1 = threading.Thread(target=self.myStart,args=(''))
		threads.append(t1)
		t2 = threading.Thread(target=self.stepCount,args=(''))
		threads.append(t2)
		for t in threads:
			t.setDaemon(True)
			t.start()
		t.join()
		self.statusBar().showMessage(_fromUtf8('分析完成...'))
		QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('分析完成'),
			QtGui.QMessageBox.Ok)

	def myStart(self):
		cp_parameters = ConfigParser.SafeConfigParser()
		cp_parameters.read(os.getcwd()+'/env.conf')
		homedir = cp_parameters.get('myconfig','reportdir')
		errlist=[]
		s = myConnect( cp_parameters.get('myconfig','currentdialog'))
		self.textBrowser_Home.append(_fromUtf8('分析开始...\r\n'))

		if cp_parameters.getboolean('myconfig','checksyse2prom'):
			try:
				GetEepromInfo(s,homedir)
			except:
				errlist.append('E2prom info')
		if cp_parameters.getboolean('myconfig','checksyshardware'):
			try:
				GetHardInfo(s,homedir)
			except:
				errlist.append('Hardware info')
		if cp_parameters.getboolean('myconfig','checksyssoftware'):
			try:
				GetSoftInfo(s,"tb_system_version",homedir)
			except:
				errlist.append('Software info')
		s.close()
		lenth = len(errlist)
		if lenth > 0:
			self.textBrowser_Home.append(_fromUtf8('获取失败列表：'))
			for i in range(lenth):
				self.textBrowser_Home.append(str(errlist[i-1]))

	#结束程序确认提示
	def closeEvent(self,event):
		reply = QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('是否确定结束程序？'),
			QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

'''
连接设置窗口
'''
class myDiaConnect(QtGui.QWidget, Ui_DialogConnect):
	def __init__(self,parent = None):
		super(myDiaConnect,self).__init__(parent)
		self.setupUi(self)
		#连接属性初始化
		my_link = ConfigParser.SafeConfigParser()
		my_link.read(os.getcwd()+'/env.conf')
		if my_link.getboolean('myconfig','openstatus'):
			curdialog = my_link.get('myconfig','currentdialog')
			curdialog = os.path.split(curdialog)
			dianame = os.path.splitext(curdialog)[0]
			if os.path.splitext(curdialog)[1] == '.netconf':
				open_link = ConfigParser.SafeConfigParser()
				open_link.read(my_link.get('myconfig','currentdialog'))
				self.lineEdit_NetName.setText(_fromUtf8(open_link.get(dianame,'subnetname')))
				self.comboBox_NetProtocol.setText(_fromUtf8(open_link.get(dianame,'subnetprotocol')))
				self.lineEdit_NetHostIP.setText(_fromUtf8(open_link.get(dianame,'subnethostip')))
				self.lineEdit_NetPort.setText(_fromUtf8(open_link.get(dianame,'subnetport')))
				self.lineEdit_NetUser.setText(_fromUtf8(open_link.get(dianame,'subnetusername')))
				self.lineEdit_NetPasswd.setText(_fromUtf8(open_link.get(dianame,'subnetpassword')))
				self.comboBox_LocalIP.setText(_fromUtf8(open_link.get(dianame,'localip')))
				self.lineEdit_PlatformIP.setText(_fromUtf8(open_link.get(dianame,'platformip')))
				self.lineEdit_ReportPath.setText(_fromUtf8(open_link.get(dianame,'reportpath')))

		else:
			self.lineEdit_NetName.setText( _fromUtf8('Dialog1'))
			self.lineEdit_NetPort.setText(_fromUtf8('22'))

			my_link.set('myconfig','currentdialog','')
			my_link.write(open(os.getcwd()+'/env.conf','w'))
			self.lineEdit_ReportPath.setText(_fromUtf8(my_link.get('myconfig','reportdir')))

		self.connect(self.lineEdit_NetName, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_NetPort, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_NetHostIP, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_NetUser, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_NetPasswd, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_PlatformIP, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)
		self.connect(self.lineEdit_ReportPath, QtCore.SIGNAL('textChanged(QString)'),self.onChanged)

		self.connect(self.comboBox_NetProtocol, QtCore.SIGNAL('activated(QString)'), self.onActivated)
		self.connect(self.pushButton_CheckPath, QtCore.SIGNAL(_fromUtf8('clicked()')), self.myAskDir)
		self.connect(self.pushButton_CheckAddress, QtCore.SIGNAL(_fromUtf8('clicked()')), self.myLocalIP)

		self.connect(self.pushButton_Connect, QtCore.SIGNAL(_fromUtf8('clicked()')), self.linkNetConfig)
		self.connect(self.pushButton_Save, QtCore.SIGNAL(_fromUtf8('clicked()')), self.saveNetConfig)

	def myLocalIP(self):
		IPlist = socket.gethostbyname_ex(socket.gethostname())[-1]
		self.comboBox_LocalIP.clear()
		self.comboBox_LocalIP.addItems(IPlist)
		self.comboBox_LocalIP.setCurrentIndex(0)

	def myAskDir(self):
		self.lineEdit_ReportPath.setText(QtGui.QFileDialog.getExistingDirectory(self, 'open dir') + '\\KDATReport\\')

	def onChanged(self):
		pass

	def onActivated(self, txt):
		for case in switch(txt):
			if case('SSH'):
				self.lineEdit_NetPort.setText(_fromUtf8('22'))
				break
			if case('TELNET'):
				self.lineEdit_NetPort.setText(_fromUtf8('23'))
				break
			if case():
				break

	def linkNetConfig(self):
		file = self.saveNetConfig()
		if file is not None:
			myConnect(file)
			my_link = ConfigParser.SafeConfigParser()
			my_link.read(os.getcwd()+'/env.conf')
			if (my_link.getboolean('myconfig','linkstatus')):
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('连接成功'),
					QtGui.QMessageBox.Ok)
			else:
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('连接失败'),
					QtGui.QMessageBox.Ok)

	def saveNetConfig(self):
		fileIsExist = False
		diaName = self.lineEdit_NetName.text()
		nettype = self.comboBox_NetProtocol.currentText()

		reportPath = self.lineEdit_ReportPath.text()

		dialogPath = reportPath+'dialogs/'
		dialogPath = str(dialogPath.replace('\\','/'))
 		
		if (os.path.exists(dialogPath) == True ):
			mylist =  os.listdir(dialogPath)
			if mylist:
				for file in mylist:
					myfile = os.path.splitext(file)
					if (str(myfile[0]).lower() == str(diaName).lower()):
						fileIsExist = True
						break
		else:
			os.makedirs(str(dialogPath))

		if not fileIsExist:
			diaName = str(self.lineEdit_NetName.text())
			diafile = dialogPath+diaName+'.netconf'
			f=open(diafile,'w')
			f.write('['+diaName+']')
			f.close()

			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(diafile)

			cp_link.set(diaName,'subnetname',diaName)
			cp_link.write(open(diafile,'w'))
			
			cp_link.set(diaName,'subnetprotocol',str(self.comboBox_NetProtocol.currentText()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'subnethostip',str(self.lineEdit_NetHostIP.text()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'subnetport',str(self.lineEdit_NetPort.text()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'subnetusername',str(self.lineEdit_NetUser.text()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'subnetpassword',str(self.lineEdit_NetPasswd.text()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'localip',str(self.comboBox_LocalIP.currentText()))
			cp_link.write(open(diafile,'w'))

			cp_link.set(diaName,'platformip',str(self.lineEdit_PlatformIP.text()))
			cp_link.write(open(diafile,'w'))

			reportPath = self.lineEdit_ReportPath.text()
			reportPath = str(reportPath.replace('\\','/'))

			cp_link.set(diaName,'reportpath',reportPath)
			cp_link.write(open(diafile,'w'))

			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			cp_link.set('myconfig','reportdir',reportPath)
			cp_link.write(open(os.getcwd()+'/env.conf','w'))

			cp_link.set('myconfig','currentdialog',diafile)
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
			self.close()
			return diafile
		else:
			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			if cp_link.getboolean('myconfig','openstatus'):
				self.close()
			else:
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('会话已存在，请重新配置！'),
					QtGui.QMessageBox.Yes)

'''
所有会话列表窗口
'''
class myDialogLinks(QtGui.QWidget, Ui_DialogLinks):
	def __init__(self,parent = None):
		super(myDialogLinks,self).__init__(parent)
		self.setupUi(self)

		#禁止关闭按钮
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMinimizeButtonHint)

		self.onRenew()

		self.connect(self.pushButton_ReNew, QtCore.SIGNAL(_fromUtf8('clicked()')), self.onRenew)

		self.connect(self.pushButton_Connect, QtCore.SIGNAL(_fromUtf8('clicked()')), self.myOpenLink)

		self.dialogConnect = myDiaConnect()
		self.connect(self.pushButton_Change, QtCore.SIGNAL(_fromUtf8('clicked()')), self.myDialogShow)

		self.connect(self.pushButton_Cancel, QtCore.SIGNAL(_fromUtf8('clicked()')), self.onClose)

		self.connect(self.listWidget_DialogList,QtCore.SIGNAL(_fromUtf8('itemSelectionChanged()')),self.lineSelect)
		try:
			currentDia =self.listWidget_DialogList.item(0).text()
			cp_link = ConfigParser.SafeConfigParser()
			cp_link.read(os.getcwd()+'/env.conf')
			diaDir = cp_link.get('myconfig','reportdir') + '/dialogs/'+currentDia
			diaDir = str(diaDir.replace('\\','/'))
			cp_link.set('myconfig','currentdialog',str(diaDir))
			cp_link.write(open(os.getcwd()+'/env.conf','w'))
		except:
			pass

	def myDialogShow(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','openstatus','True')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		self.dialogConnect.show()

	def myOpenLink(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		file = cp_link.get('myconfig','currentdialog')
		if file is not None:
			myConnect(file)
			my_link = ConfigParser.SafeConfigParser()
			my_link.read(os.getcwd()+'/env.conf')
			if (my_link.getboolean('myconfig','linkstatus')):
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('连接成功'),
					QtGui.QMessageBox.Ok)
				self.close()
			else:
				QtGui.QMessageBox.question(self,_fromUtf8('Tips'),_fromUtf8('连接失败,请检查配置信息'),
					QtGui.QMessageBox.Ok)

	def lineSelect(self):
		currentDia = self.listWidget_DialogList.item(self.listWidget_DialogList.currentRow()).text()
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		diaDir = cp_link.get('myconfig','reportdir') + '/dialogs/'+currentDia
		diaDir = str(diaDir.replace('\\','/'))
		cp_link.set('myconfig','currentdialog',str(diaDir))
		cp_link.write(open(os.getcwd()+'/env.conf','w'))

	def onRenew(self):
		my_link = ConfigParser.SafeConfigParser()
		my_link.read(os.getcwd()+'/env.conf')
		dialoglist = os.listdir(my_link.get('myconfig','reportdir')+'/dialogs')
		self.listWidget_DialogList.clear()
		self.listWidget_DialogList.addItems(dialoglist)
		self.listWidget_DialogList.setCurrentRow(0)

	def onClose(self):
		cp_link = ConfigParser.SafeConfigParser()
		cp_link.read(os.getcwd()+'/env.conf')
		cp_link.set('myconfig','openstatus','False')
		cp_link.write(open(os.getcwd()+'/env.conf','w'))
		self.close()

'''
邮件配置发送窗口
'''
class myEmail(QtGui.QWidget, Ui_DialogEmail):
	def __init__(self,parent = None):
		super(myEmail,self).__init__(parent)
		self.setupUi(self)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowMinimizeButtonHint)
		self.connect(self.pushButton_EmailCancel, QtCore.SIGNAL(_fromUtf8('clicked()')), self.onClose)
		self.connect(self.pushButton_EmailSend, QtCore.SIGNAL(_fromUtf8('clicked()')), self.onClose)

	def onClose(self):
		self.close()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myshow = myWindow()
	myshow.show()
	sys.exit(app.exec_())