#!/usr/bin/env python
# -*- coding: cp936 -*-
'''
<Auther> : guolei
<Function> : 
    Used to finish net test projects with iperf.This script is used for windows,
	and this port must be the device who will be test and an other port best for 
	linux.This is the enviroment for my test all above.
'''
import sys
import threading
import os
import time
import serial
import encodings
import re
import socket
import string
import linecache
import pyh
import xlsxwriter
import traceback

SER_ALIVE = []
LOSSRATE = []

'''
=======================================================
================Iperf Paramiters Settings =============
=======================================================
'''
TestMod = '-u'						#Set test mode(TCP:'';UDP:'-u')
DevType = 'cli'						#Set DUT type(Server:'ser';Client:'cli')
DstIP = '2.1.1.9'	 				#Set your PC IP
DstIP2 = '2.1.1.10'					#Set DUT IP
TestTime = '5'						#Set test time(sec)
TestSpeed = 100						#Set packages send speed
TestFrameArray =('64','128','256','512','1024','1280','1472')
#TestFrameArray =('1280','1472')
									#Set test frame list
Dir_Path = './resoult/'				#Set script path
'''
=======================================================
================ Serail Paramiters Config =============
=======================================================
'''
Serail_Com_Port = '/dev/ttyUSB0'			#Set serial port
Serail_Com_Baud_Rate = 38400		#Set baud rate
Serail_Com_Data_Bits = 8			#Set below default
Serail_Com_Parity = 'N'
Serail_Com_Stop_Bits = 1
Serail_Com_Timeout = 1
Serail_Com_Xonxoff = 0
Serail_Com_Rtscts = 0
'''
=======================================================
===================  Log File Config ==================
======================================================= 
'''
Log_File_Name = 'ser_read_log' 		#Set log file name
Iperf_Resoult_Name = 'iperf_resoult'
Top_Log_Name = 'top_resoult_log'
Excel_Report_Name = 'Throughput_Report'
Top_Data_Name = 'Top_data'
lows = 8
'''
=======================================================
================ MultiThreading Setting ===============
======================================================= 
'''
def threadFunc(num):
    global total, mutex
    #print names of threads
    print threading.currentThread().getName()
  
    for x in xrange(0, int(num)):
        #get mutex
        mutex.acquire()
        total = total + 1
        #free mutex
        mutex.release()

def main(num):
    #define global variable
	global total, mutex
	total = 0
    #greate mutex
	mutex = threading.Lock()
    #define thread pool
	threads = []
    #greate thread objects
	threads.append(threading.Thread(target=SerialRead, args=(1,)))
	threads.append(threading.Thread(target=SerialWrite, args=(1,)))
    #start all threads
	for t in threads:
		t.start()
    #The main thread waits for all sub thread exits
	for t in threads:
		t.join()

def SerialRead(arg):
	while SER_ALIVE:
		try:
			n = ser.inWaiting()
			if not n:
				continue
#			print 'n = ',n
			fileHandle = open ( Iperf_Log_File, 'a' )
			read_str = ser.readall()
			print read_str
			fileHandle.write(read_str)
			if TestMod is '':
				pass
			else:
				if read_str.rfind('(')>0 and read_str.rfind('%)')>0:
					global LOSSRATE
					LOSSRATE =read_str[read_str.find('(')+1:read_str.find('%)')]
#				print 'LOSSRATE in read is ',LOSSRATE
			fileHandle.close()
			read_str = ''
		except:
			print '=== STEP ERROR INFO START ==='
			traceback.print_exc()
			print '=== STEP ERROR INFO END ==='

def SerialWrite(arg):
	try:
		if TestMod is '':
			print '==========Now I am testing for TCP !==========\n'
		else:
			print '==========Now I am testing for UDP !==========\n'
		time.sleep(0.5)
		ser.write('cd /usr/bin\n')
		time.sleep(0.5)
		ser.write('ls\n')
		time.sleep(0.5)
		ser.write('date > /ramdisk/'+Top_Log_Name+'.log&\n')
		time.sleep(0.5)
		ser.write('top -b >> /ramdisk/'+Top_Log_Name+'.log&\n')
		time.sleep(5)
		AllTest()
#		ManuWrite()
	except:
		print '=== STEP ERROR INFO START ==='
		traceback.print_exc()
		print '=== STEP ERROR INFO END ==='

def ManuWrite():
	while SER_ALIVE:
		try:
			strSerial = ''
			Exit = 'exit'
#			print 'I am SerialWrite Thread!\n'
			strSerial = raw_input()
#			print strSerial
#			print ser.write('cd /usr/bin\nls\n')
			if strSerial == Exit:
				print 'Now Exit !'
				sys.exit(1)
			ser.write(strSerial+'\n')
		except IOError('Serial Write Error'):
			break

def CopyTopLog(srcfile,dstfile,dstfile2):
	try:
		#copy top log to top file
		thefile= open(srcfile,'r')
		count = len(thefile.readlines())
		mysstr= 'Now_cut_top_log\n'
		copylog=linecache.getlines(srcfile)
		copylog=[copylog[i] for i in range(len(copylog)) if copylog[i]!='\n']
		renum=copylog.index(mysstr)
		open(dstfile,'w')
		for n in range(renum,len(copylog)):
			open(dstfile,'a').write(copylog[n])
		open(dstfile,'a').close()
		#copy top info to data file
		thefile= open(dstfile,'r')
		count = len(thefile.readlines())
		sstr1= "Packet_Size"
		sstr2= "CPU:"
		for i in range(count):
			renum1 =linecache.getline(dstfile,i).find(sstr1)
			if renum1 is not -1:
				renum2 =linecache.getline(dstfile,i).find(sstr2)
				n=i
				while renum2 is -1:
					n=n-1
					renum2 =linecache.getline(dstfile,n).find(sstr2)
				n=n-1
				renum2 =linecache.getline(dstfile,i).find(sstr2)
				while renum2 is -1:
					n=n-1
					renum2 =linecache.getline(dstfile,n).find(sstr2)
				open(dstfile2,'a').write(linecache.getline(dstfile,n))
				open(dstfile2,'a').close()		
	except:
		print '=== STEP ERROR INFO START ==='
		traceback.print_exc()
		print '=== STEP ERROR INFO END ==='

def CopyResoultData(srcfile,dstfile):
	try:
		thefile= open(srcfile,'r')
		count = len(thefile.readlines())
		sstr1= "Speed is:"
		if TestMod is '':
			sstr2= "bits/sec"
		else:
			sstr2= "(0%)"
		sstr3= "Receiving"
		open(dstfile,'w')
		for i in range(count):
			renum1 =linecache.getline(srcfile,i).find(sstr1)
			if renum1 is not -1:
				open(dstfile,'a').write(linecache.getline(srcfile,i))
				open(dstfile,'a').close()
#				print '=============Find Speed==============='
				renum2 =linecache.getline(srcfile,i).find(sstr2)
				n=i
				while renum2 is -1:
					n=n-1
#					print 'n1 is :',n
					if (n < 1) or (n > count):
						print '========== Not Find bits/sec =========='
						break
					renum2 =linecache.getline(srcfile,n).find(sstr2)
				open(dstfile,'a').write(linecache.getline(srcfile,n))
				open(dstfile,'a').close()
#				print '=============Find bits/sec==============='
				renum3 =linecache.getline(srcfile,i).find(sstr3)
				while renum3 is -1:
					n=n+1
#					print 'n2 is :',n
					if (n < 1) or (n > count):
						print '========== Not Find Receiving =========='
						break
					renum3 =linecache.getline(srcfile,n).find(sstr3)
				open(dstfile,'a').write(linecache.getline(srcfile,n))
				open(dstfile,'a').close()
#				print 'Line num is :',i
#				print '=============Find Receiving==============='
	except:
		print '=== STEP ERROR INFO START ==='
		traceback.print_exc()
		print '=== STEP ERROR INFO END ==='

def CreateExcelTcp(srcfile,srcfile2,dstfile):
	myList = []
	head_list = ['FrameSize(byte)','BandWidth(Mbps)','Throughput(Mbites/s)','CPU(%)','SIRQ(%)']
	myList.append(head_list)

	fileHandle = open ( srcfile, 'r' )
	count = len(fileHandle.readlines())
	for n in range(1,count,3):
		temlist = ['']*(lows-3)
		read_str = linecache.getline(srcfile,n)
		temlist[1] = int(read_str[read_str.find(':')+1:read_str.find('Mbps')].strip())
		n=n+1
		read_str = linecache.getline(srcfile,n)
		temlist[2] = float(read_str[read_str.find('Bytes')+5:read_str.find('bits/sec')-1].strip())
		n=n+1
		read_str = linecache.getline(srcfile,n)
		temlist[0] = int(read_str[read_str.find('Receiving')+9:read_str.find('byte')].strip())
		if n%3 == 0:
			fileHandle2 = open ( srcfile2, 'r' )
			count = len(fileHandle2.readlines())
			read_str = linecache.getline(srcfile2,n/3)
			temlist[3] = read_str[read_str.find('nic')+3:read_str.find('% idle')].strip()
			temp = string.atof(temlist[3])
			temlist[3]=float(100 - temp)
			temlist[4] = float(read_str[read_str.find('% irq')+5:read_str.find('% sirq')].strip())
			myList.append(temlist)
	fileHandle.close()
	
	workbook = xlsxwriter.Workbook(dstfile)
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})
	
	for i in range(0,len(myList),1):
		temp = '%d' %(i+1)
		worksheet.write_row('A'+temp, myList[i])
	
	i='%d' %(i+1)
	
	#######################################################################
	#
	# Create a new scatter chart.
	#
	chart1 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart1.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$C$2:$C$'+i,
	})

	# Add a chart title and some axis labels.
	chart1.set_title ({'name': 'Throughput'})
	chart1.set_x_axis({'name': 'FrameSize(byte)'})
	chart1.set_y_axis({'name': 'Throughput(Mbites/s)'})

	# Set an Excel chart style.
	chart1.set_style(11)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('A11', chart1, {'x_offset': 25, 'y_offset': 10})
	
	#######################################################################
	#
	# Create a scatter chart sub-type with straight lines and markers.
	#
	chart2 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart2.add_series({
    'name':       '=Sheet1!$D$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$D$2:$D$'+i,
	})

	# Add a chart title and some axis labels.
	chart2.set_title ({'name': 'CPU'})
	chart2.set_x_axis({'name': 'FrameSize(byte)'})
	chart2.set_y_axis({'name': 'CPU(ms)'})

	# Set an Excel chart style.
	chart2.set_style(12)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('A27', chart2, {'x_offset': 25, 'y_offset': 10})
	
	#######################################################################
	#
	# Create a new scatter chart.
	#
	chart3 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart3.add_series({
    'name':       '=Sheet1!$E$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$E$2:$E$'+i,
	})

	# Add a chart title and some axis labels.
	chart3.set_title ({'name': 'SIRQ'})
	chart3.set_x_axis({'name': 'FrameSize(byte)'})
	chart3.set_y_axis({'name': 'SIRQ(%)'})

	# Set an Excel chart style.
	chart3.set_style(11)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('I11', chart3, {'x_offset': 25, 'y_offset': 10})

	workbook.close()

def CreateExcelUdp(srcfile,srcfile2,dstfile):
	myList = []
	head_list = ['FrameSize(byte)','BandWidth(Mbps)','Throughput(Mbites/s)','Jitters(ms)',
									'PacketLoss','LossRate(%)','CPU(%)','SIRQ(%)']
	myList.append(head_list)

	fileHandle = open ( srcfile, 'r' )
	count = len(fileHandle.readlines())
	for n in range(1,count,3):
		temlist = ['']*lows
		read_str = linecache.getline(srcfile,n)
		temlist[1] = int(read_str[read_str.find(':')+1:read_str.find('Mbps')].strip())
		n=n+1
		read_str = linecache.getline(srcfile,n)
		temlist[2] = float(read_str[read_str.find('Bytes')+5:read_str.find('bits/sec')-1].strip())
		temlist[3] = float(read_str[read_str.find('bits/sec')+8:read_str.find('ms')].strip())
		temlist[4] = read_str[read_str.find('ms')+2:read_str.find('(')].strip()
		temlist[5] = float(read_str[read_str.find('(')+1:read_str.find('%)')].strip())
		n=n+1
		read_str = linecache.getline(srcfile,n)
		temlist[0] = int(read_str[read_str.find('Receiving')+9:read_str.find('by')-1].strip())
		if n%3 == 0:
			fileHandle2 = open ( srcfile2, 'r' )
			count = len(fileHandle2.readlines())
			read_str = linecache.getline(srcfile2,n/3)
			temlist[6] = read_str[read_str.find('nic')+3:read_str.find('% idle')].strip()
			temp = string.atof(temlist[6])
			temlist[6]=float(100 - temp)
			temlist[7] = float(read_str[read_str.find('% irq')+5:read_str.find('% sirq')].strip())
			myList.append(temlist)
	fileHandle.close()
	
	workbook = xlsxwriter.Workbook(dstfile)
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})
	
	for i in range(0,len(myList),1):
		temp = '%d' %(i+1)
		worksheet.write_row('A'+temp, myList[i])
	
	i='%d' %(i+1)
#	print '============Read Ending=============='
	#######################################################################
	#
	# Create a new scatter chart.
	#
	chart1 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart1.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$C$2:$C$'+i,
	})

	# Add a chart title and some axis labels.
	chart1.set_title ({'name': 'Throughput'})
	chart1.set_x_axis({'name': 'FrameSize(byte)'})
	chart1.set_y_axis({'name': 'Throughput(Mbites/s)'})

	# Set an Excel chart style.
	chart1.set_style(11)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('A11', chart1, {'x_offset': 25, 'y_offset': 10})
	
	#######################################################################
	#
	# Create a scatter chart sub-type with straight lines and markers.
	#
	chart2 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart2.add_series({
    'name':       '=Sheet1!$D$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$D$2:$D$'+i,
	})

	# Add a chart title and some axis labels.
	chart2.set_title ({'name': 'Jitters'})
	chart2.set_x_axis({'name': 'FrameSize(byte)'})
	chart2.set_y_axis({'name': 'Jitters(ms)'})

	# Set an Excel chart style.
	chart2.set_style(12)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('A27', chart2, {'x_offset': 25, 'y_offset': 10})
	
	#######################################################################
	#
	# Create a new scatter chart.
	#
	chart3 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart3.add_series({
    'name':       '=Sheet1!$G$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$G$2:$G$'+i,
	})

	# Add a chart title and some axis labels.
	chart3.set_title ({'name': 'CPU'})
	chart3.set_x_axis({'name': 'FrameSize(byte)'})
	chart3.set_y_axis({'name': 'CPU(%)'})

	# Set an Excel chart style.
	chart3.set_style(11)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('I11', chart3, {'x_offset': 25, 'y_offset': 10})
	
	#######################################################################
	#
	# Create a new scatter chart.
	#
	chart4 = workbook.add_chart({'type': 'scatter','subtype': 'straight'})

	# Configure the first series.
	chart4.add_series({
    'name':       '=Sheet1!$H$1',
    'categories': '=Sheet1!$A$2:$A$'+i,
    'values':     '=Sheet1!$H$2:$H$'+i,
	})

	# Add a chart title and some axis labels.
	chart4.set_title ({'name': 'SIRQ'})
	chart4.set_x_axis({'name': 'FrameSize(byte)'})
	chart4.set_y_axis({'name': 'SIRQ(%)'})

	# Set an Excel chart style.
	chart4.set_style(11)

	# Insert the chart into the worksheet (with an offset).
	worksheet.insert_chart('I27', chart4, {'x_offset': 25, 'y_offset': 10})
	
	workbook.close()
		
def AllTest():
	TestTimeTmp = string.atoi(TestTime)
	n = len(TestFrameArray)
	if TestMod is '':
		if DevType is 'ser':
			ser.write('./iperf -s&\n')
		elif DevType is 'cli':
			os.system('iperf -s&\n')
		else:
			print '=============DevType is invalid!============='
			os._exit(0)
		time.sleep(0.5)
		for i in range(0,n,1):
			TestSpeedTmp1 = '%d' %TestSpeed
			if DevType is 'ser':
				ser.write('echo iperf '+TestMod+' -c '+DstIP2+' -t '+ TestTime +' -l '+TestFrameArray[i]+'\n')
				os.system('iperf '+TestMod+' -c '+DstIP2+' -t '+ TestTime +' -l '+TestFrameArray[i]+'\n')
			elif DevType is 'cli':
				ser.write('./iperf '+TestMod+' -c '+DstIP+' -t '+ TestTime +' -l '+TestFrameArray[i]+'\n')
			else:
				print '=============DevType is invalid!============='
				os._exit(0)
			time.sleep(TestTimeTmp+5)
			ser.write('echo Packet_Size is: '+TestFrameArray[i]+'byte >> /ramdisk/'+
																				Top_Log_Name+'.log\n')
			time.sleep(1)
			fileHandle = open( Iperf_Log_File,'a')
			time.sleep(0.5)
			fileHandle.write('Receiving '+TestFrameArray[i]+'byte datagrams\n')
			time.sleep(0.5)
			fileHandle.write('Speed is:'+TestSpeedTmp1+'Mbps\n')
			time.sleep(0.5)
			fileHandle.close()
	else:
		if DevType is 'ser':
			ser.write('./iperf -s -u&\n')
		elif DevType is 'cli':
			os.system('iperf -s -u&\n')
		else:
			print '=============DevType is invalid!============='
			os._exit(0)
		for i in range(0,n,1):
			TestSpeedTmp = 0	#speed in num
			TestSpeedTmp1= ''	#speed in char
			TestSpeedTmp2 = 0	#min speed
			TestSpeedTmp3 = 100	#max speed
			TestSpeedTmp = TestSpeed
			tmp = 2
			TestSpeedTmp1 = '%d' %TestSpeedTmp
#			print 'TestSpeed is ',TestSpeedTmp
#			print 'LOSSRATE is ',LOSSRATE
			if DevType is 'ser':
				ser.write('echo iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1+'M'+' -l '
																				+TestFrameArray[i]+'\n')
				os.system('iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1+'M'+' -l '
																				+TestFrameArray[i]+'\n')
			elif DevType is 'cli':
				ser.write('./iperf '+TestMod+' -c '+DstIP+' -t '+TestTime+' -b '+TestSpeedTmp1+'M'+' -l '
																				+TestFrameArray[i]+'\n')
			else:
				print '=============DevType is invalid!============='
				os._exit(0)
			time.sleep(TestTimeTmp+5)
#			global REPORT_FLAG
#			REPORT_FLAG = 0
#			print '========================Flag 1======================='
#			print 'LOSSRATE is ',LOSSRATE
			while True:
				if tmp < 2:
					break
#				print '========================Flag 2======================='
#				print 'LOSSRATE is ',LOSSRATE
				#if LOSSRATE > 0,decrease TestSpeed or break
				while (LOSSRATE > '0'):
					try:
#						print '================LOSSRATE > 0==============='
						TestSpeedTmp3 = TestSpeedTmp
						tmp = TestSpeedTmp - TestSpeedTmp2
						if tmp > 1:
							TestSpeedTmp = (TestSpeedTmp + TestSpeedTmp2) / 2
						else:
							TestSpeedTmp = TestSpeedTmp2
							TestSpeedTmp1 = '%d' %TestSpeedTmp
							ser.write('echo Receiving '+TestFrameArray[i]+' byte datagrams\n')
							time.sleep(0.5)
							ser.write('echo Packet_Size is: '+TestFrameArray[i]+'byte >> /ramdisk/'+
																				Top_Log_Name+'.log\n')
							time.sleep(0.5)
							fileHandle = open( Iperf_Log_File,'a')
							fileHandle.write('Speed is:'+TestSpeedTmp1+'Mbps\n')
							fileHandle.close()
#							print 'test end  != 0'
							break
						TestSpeedTmp1 = '%d' %TestSpeedTmp
						if DevType is 'ser':
							ser.write('echo iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1
																	+'M'+' -l '+TestFrameArray[i]+'\n')
							os.system('iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1
																	+'M'+' -l '+TestFrameArray[i]+'\n')
						elif DevType is 'cli':
							ser.write('./iperf '+TestMod+' -c '+DstIP+' -t '+TestTime+' -b '+TestSpeedTmp1
																	+'M'+' -l '+TestFrameArray[i]+'\n')
						else:
							print '=============DevType is invalid!============='
							os._exit(0)
						time.sleep(TestTimeTmp+5)
					except IOError('Set Value Error'):
						break
				#if LOSSRATE = 0,increase TestSpeed or break
				while (LOSSRATE == '0'):
					try:
#						print '================LOSSRATE = 0==============='
						TestSpeedTmp2 = TestSpeedTmp
						tmp = TestSpeedTmp3 - TestSpeedTmp
						if tmp > 1:
							TestSpeedTmp = (TestSpeedTmp + TestSpeedTmp3) / 2
							TestSpeedTmp1 = '%d' %TestSpeedTmp
							if DevType is 'ser':
								ser.write('echo iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1
																		+'M'+' -l '+TestFrameArray[i]+'\n')
								os.system('iperf '+TestMod+' -c '+DstIP2+' -t '+TestTime+' -b '+TestSpeedTmp1
																		+'M'+' -l '+TestFrameArray[i]+'\n')
							elif DevType is 'cli':
								ser.write('./iperf '+TestMod+' -c '+DstIP+' -t '+TestTime+' -b '+TestSpeedTmp1
																		+'M'+' -l '+TestFrameArray[i]+'\n')
							else:
								print '=============DevType is invalid!============='
								os._exit(0)
							time.sleep(TestTimeTmp+5)
						else:
							TestSpeedTmp1 = '%d' %TestSpeedTmp
							ser.write('echo Receiving '+TestFrameArray[i]+' byte datagrams\n')
							time.sleep(0.5)
							ser.write('echo Packet_Size is: '+TestFrameArray[i]+'byte >> /ramdisk/'+
																				Top_Log_Name+'.log\n')
							time.sleep(0.5)
							fileHandle = open ( Iperf_Log_File, 'a' )
							fileHandle.write('Speed is:'+TestSpeedTmp1+'Mbps\n')
							fileHandle.close()
#							print 'test end == 0'
							break
					except:
						print '=== STEP ERROR INFO START ==='
						traceback.print_exc()
						print '=== STEP ERROR INFO END ==='
						break
			time.sleep(0.5)
	ser.write('killall top\n')
	time.sleep(0.5)
	ser.write('killall iperf\n')
	time.sleep(0.5)
	ser.write('date >> /ramdisk/'+Top_Log_Name+'.log\n')
	time.sleep(0.5)
	ser.write('echo "Now_cut_top_log"\n')
	time.sleep(0.5)
	ser.write('cat /ramdisk/'+Top_Log_Name+'.log\n')
	time.sleep(2)
	global SER_ALIVE
	SER_ALIVE = False
#	print 'SER_ALIVE is ',SER_ALIVE

if __name__ == '__main__':
	if (os.path.exists(DIR_path)) is not True:
		os.makedirs(DIR_path)
	#open serial
	try:
		ser = serial.Serial(Serail_Com_Port,Serail_Com_Baud_Rate,Serail_Com_Data_Bits,
                            Serail_Com_Parity,Serail_Com_Stop_Bits,Serail_Com_Timeout,
                            Serail_Com_Xonxoff,Serail_Com_Rtscts)
		SER_ALIVE = True
		print 'Open Serial Success!\n'
	except Exception, e:
		print 'Open Serial Failed!\n'
		exit(1)
	
	endtime = time.strftime('%m%d%H%M%S',time.localtime(time.time()))
	
	#set save logs path
	if TestMod is '-u':
		Excel_Report_Name = Excel_Report_Name+'_UDP'
	else:
		Excel_Report_Name = Excel_Report_Name+'_TCP'
	Absolute_Path = Dir_Path+endtime+'/'
	os.mkdir(Absolute_Path)
	Iperf_Log_File =Absolute_Path+ Log_File_Name+'.log'
	Iperf_Resoult_File =Absolute_Path+ Iperf_Resoult_Name+'.log'
	Top_Log_File =Absolute_Path+ Top_Log_Name+'.log'
	Excel_Report_File = Absolute_Path+ Excel_Report_Name+'.xlsx'
	Top_Data_File = Absolute_Path+ Top_Data_Name+'.log'
	
	#save log infomation as Save_File_Name
	fileHandle = open ( Iperf_Log_File, 'w' )
	fileHandle.write(time.strftime('\n%Z  %Y %m-%d %H:%M:%S %A \r\n\n',
                                   time.localtime(time.time())))
	fileHandle.close()
	
    #start serial read and write threads
	main(2)
	ser.close()
	print 'Now! Copying top log to file :',Top_Log_Name,'.log'
	print 'waiting......'
	CopyTopLog(Iperf_Log_File,Top_Log_File,Top_Data_File)
	print 'Top log copying done!!!\n'
	
	print 'Now! Copying iperf resoult data to file :',Iperf_Resoult_Name,'.log'
	print 'waiting......'
	CopyResoultData(Iperf_Log_File,Iperf_Resoult_File)
	print 'Iperf resoult data copying done!!!\n'
	
	print 'Now! Generating report :',Excel_Report_Name,'.xlsx'
	print 'waiting......'
	if TestMod is '':
		CreateExcelTcp(Iperf_Resoult_File,Top_Data_File,Excel_Report_File)
	else:
		CreateExcelUdp(Iperf_Resoult_File,Top_Data_File,Excel_Report_File)
	print 'Generating report creating done!!!\n'
	
	fileHandle = open ( Iperf_Log_File, 'a' )
	fileHandle.write(time.strftime('\n\n%Z  %Y %m-%d %H:%M:%S %A \r\n',
                                   time.localtime(time.time())))
	fileHandle.close()
	os.system('cd resoult\n')
	time.sleep(0.5)
	os.system('sudo chgrp guolei * -R\n')
	time.sleep(0.5)
	os.system('sudo chown guolei * -R\n')
	print 'All Test is done!!!\n'
	os._exit(0)
