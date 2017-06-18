# -*- coding: UTF-8 -*-

import time
import ConfigParser
from database.database import *
from modules.myConnect import my17230,myFtp

def GetVersionInfo(link,table):
	'''获取内核版本信息'''
	try:
		execmd = "cat /proc/version"
		stdin, stdout, stderr = link.exec_command (execmd)
		stdin.write("Y")
		DataInsert('system',table,[(1,'version',stdout.read())])
	except Exception:
		pass

	'''获取cmdline信息'''
	try:
		execmd = "cat /proc/cmdline"
		stdin, stdout, stderr = link.exec_command (execmd)
		DataInsert('system',table,[(2,"cmdline",stdout.read())])
	except Exception:
		pass

	'''获取busybox信息'''
	try:
		execmd = "busybox > /ramdisk/system_busyboxinfo.log"
		stdin, stdout, stderr = link.exec_command (execmd)
	except Exception:
		pass

def GetVersion17230(homedir):
	f1=file(homedir+"/log/systemlog/system_17230info.log","w")
	f1.write("[versionlog]\n\r")
	f1.close()
	time.sleep(.1)

	f=file(homedir+"/log/systemlog/system_17230info.log","a+")
	try:
		f.write(my17230(homedir,"ipcver"))
		time.sleep(.1)
		my17230(homedir,"testapi")
		f.write(my17230(homedir,"showver"))
		time.sleep(.1)
		f.write(my17230(homedir,"mc_ver"))
		time.sleep(.1)
		f.write(my17230(homedir,"medianetver"))
		time.sleep(.1)
	except Exception:
		pass
	f.close()

def FtpGet(homedir):
	'''获取并删除日志文件'''
	try:
		myFtp("get","system",homedir,"system_busyboxinfo.log")
	except Exception:
		pass

def GetSoftInfo(link,table,homedir):
	init(table)
	
	GetVersionInfo(link,table)
	#GetVersion17230(homedir)
	#FtpGet(homedir)
	#VersionDataEntry(homedir)
	#查看数据库表中数据
	#fetchall_test(table)

def VersionDataEntry(homedir):
	file = homedir+"/log/systemlog/system_17230info.log"
	with open(file,"r") as f:
		lines = f.readlines()

	with open(file,"w") as f_w:
		for line in lines:
			if ":" in line or "[versionlog]" in line:
				f_w.write(line)
			continue

	cp_ver = ConfigParser.SafeConfigParser()
	cp_ver.read(homedir+'/log/systemlog/system_17230info.log')
	print cp_ver.get('versionlog','ipcsrv')
	print cp_ver.get('versionlog','ipccore')
	print cp_ver.get('versionlog','ispVersion')
	print cp_ver.get('versionlog','Drvlib     ver')
	print cp_ver.get('versionlog','Sysdbg     ver')
	print cp_ver.get('versionlog','Rpdata     ver')
	print cp_ver.get('versionlog','Rpstream   ver')
	print cp_ver.get('versionlog','NETCBB     ver')
	print cp_ver.get('versionlog','PPPOE      ver')
	print cp_ver.get('versionlog','DDNS       ver')
	print cp_ver.get('versionlog','upnp       ver')
	print cp_ver.get('versionlog','wifi lib version')
	print cp_ver.get('versionlog','MediaCtrl Module Version')
	print cp_ver.get('versionlog','Medianet(C) 1.0.0.20140312 compile time')