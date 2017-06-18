# -*- coding: UTF-8 -*-
import os,ConfigParser
from modules.myConnect import myFtp

def SaveHardInfo(link,homedir):
	'''获取cpuinfo'''
	try:
		execmd = "cat /proc/cpuinfo > /ramdisk/system_cpuinfo.log"
		stdin, stdout, stderr = link.exec_command (execmd)
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

	'''获取meminfo'''
	try:
		execmd = "cat /proc/meminfo > /ramdisk/system_meminfo.log"
		stdin, stdout, stderr = link.exec_command (execmd)
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

	'''获取mtdinfo'''
	try:
		execmd = "cat /proc/mtd > /ramdisk/system_mtd.log"
		stdin, stdout, stderr = link.exec_command (execmd)
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))
	
	'''获取partition info'''
	try:
		execmd = "cat /proc/partitions > /ramdisk/system_partitions.log"
		stdin, stdout, stderr = link.exec_command (execmd)
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

def HardGet(homedir):
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')

	'''获取并删除日志文件'''
	try:
		myFtp("get","system",homedir,"system_cpuinfo.log")
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

	try:
		myFtp("get","system",homedir,"system_meminfo.log")
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

	try:
		myFtp("get","system",homedir,"system_mtd.log")
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

	try:
		myFtp("get","system",homedir,"system_partitions.log")
	except Exception:
		pass
	cp_link = ConfigParser.SafeConfigParser()
	cp_link.read(os.getcwd()+'/env.conf')
	cp_link.set('myconfig','currentstep',str(cp_link.getint('myconfig','currentstep')+1))
	cp_link.write(open(os.getcwd()+'/env.conf','w'))

def GetHardInfo(link,homedir):
	SaveHardInfo(link,homedir)
	HardGet(homedir)