# -*- coding: UTF-8 -*-

import os,sys,paramiko,telnetlib,time
import ConfigParser
from modules.myClass import *
from ftplib import FTP
import socket

FTP_Port='21'
ramdisk='/ramdisk'
buffsize=1024

DEBUG = False

def myConnect(myfile):
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(myfile)
	filename = os.path.split(myfile)[1]
	mydialog = os.path.splitext(filename)[0]
	myext = os.path.splitext(filename)[1]

	for case in switch(cp_link.get(mydialog,'SubNetProtocol')):
		if case('SSH'):
			'''使用ssh登录'''
			hostname = cp_link.get(mydialog,'SubNetHostIP')
			port = cp_link.getint(mydialog,'SubNetPort')  
			username = cp_link.get(mydialog,'SubNetUserName')  
			password = cp_link.get(mydialog,'SubNetPassWord')
			pathParamiko = cp_link.get(mydialog,'reportpath')+"/paramiko.log"
			paramiko.util.log_to_file(pathParamiko)  

			cp_env = ConfigParser.SafeConfigParser()
			cp_env.read(os.getcwd()+'/env.conf')
			try:
				
				s = paramiko.SSHClient()  
				s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				s.connect(hostname, port, username, password)

				cp_env.set('myconfig','linkstatus','True')
				cp_env.write(open(os.getcwd()+'/env.conf','w'))
			except Exception,e:
				cp_env.set('myconfig','linkstatus','False')
				cp_env.write(open(os.getcwd()+'/env.conf','w'))
			break
		if case('TELNET'):
			break
		if case('SERIAL'):
			break
		if case():
			break
	return s


def ftp_download(ftp,HOST_IP,UserName,Password,remotefile,localpath):
	try:
		ftp.connect(HOST_IP, FTP_Port)
	except (socket.error, socket.gaierror):  
		print u'错误:ftp:连接"%s"失败' % HOST_IP  
		sys.exit(0) 

	ftp.login(UserName,Password)
	ftp.cwd(ramdisk)
	file_write=open(localpath+remotefile,'wb').write
	ftp.retrbinary('RETR '+ remotefile, file_write, buffsize)
	ftp.delete(remotefile)

	ftp.quit()

def myFtp(trans,type,homedir,remotefile):
	cp_parameters = ConfigParser.SafeConfigParser()
	cp_parameters.read(os.getcwd()+'/env.conf')

	cp_link = ConfigParser.SafeConfigParser()
	myfile = cp_parameters.get('myconfig','currentdialog')
	filename = os.path.split(myfile)[1]
	mydialog = os.path.splitext(filename)[0]
	cp_link.read(myfile)
	for case in switch(type):
		if case("system"):
			localpath = homedir+"/log/systemlog/"
			break
		if case():
			break

	ftp=FTP()
	HOST_IP =cp_link.get(mydialog,'subnethostip')
	UserName=cp_link.get(mydialog,'subnetusername')
	Password=cp_link.get(mydialog,'subnetpassword')
	
	if(trans == "get"):
		ftp_download(ftp,HOST_IP,UserName,Password,remotefile,localpath)
	#elif(trans == "put"):
	#	uploadfile( remotepath, localpath)
	else:
		print u"错误:myFtp:参数trans传入错误"

def my17230(homedir,commands):
	cp_parameters = ConfigParser.SafeConfigParser()
	cp_parameters.read(os.getcwd()+'/env.conf')

	cp_link = ConfigParser.SafeConfigParser()
	myfile = cp_parameters.get('myconfig','currentdialog')
	filename = os.path.split(myfile)[1]
	mydialog = os.path.splitext(filename)[0]
	cp_link.read(myfile)

	hostip = cp_link.get(mydialog,'SubNetHostIP')  
	username = cp_link.get(mydialog,'SubNetUserName')  
	password = cp_link.get(mydialog,'SubNetPassWord')
	finish = "bin->"

	# 连接Telnet服务器  
	tn = telnetlib.Telnet(hostip,17230)# >> homedir+'\\log\\softwarelog\\my17230.log'
	tn.set_debuglevel(5)
	# 输入登录用户名  
	tn.read_until('Username:')  
	tn.write(username + '\r')  

	if(password != ''):
		# 输入登录密码  
		tn.read_until('Password:')  
		tn.write(password + '\r')          

	# 登录完毕后执行命令  
	tn.read_until(finish)  
	tn.write(commands + '\r')
	time.sleep(.1)
	result = tn.read_very_eager()
	tn.write('bye\r')
	tn.close()
	return result