# -*- coding: UTF-8 -*-

import os,ConfigParser
from modules.myConnect import myFtp

def SaveEepromInfo(link,homedir):
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	
	'''获取eeprom信息'''
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))
	try:
		execmd = "hwinfo > /ramdisk/system_eeprom.log"
		stdin, stdout, stderr = link.exec_command (execmd)
		stdin.write("Y")
	except Exception:
		pass

def EepromGet(homedir):
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	'''获取并删除日志文件'''
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))
	try:
		myFtp("get","system",homedir,"system_eeprom.log")
	except Exception:
		pass

def GetEepromInfo(link,homedir):
	SaveEepromInfo(link,homedir)
	EepromGet(homedir)