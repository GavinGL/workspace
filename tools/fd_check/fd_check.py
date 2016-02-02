#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 *
 * Copyright (c) 2009-~ Guo lei
 *
 * Author:       Guo lei<guolei@kedacom.com>
 * Created Time: 2016年02月01日 星期一 19时38分56秒
 * File Name:    fd_check.py
 *
 * Description:  
 *
'''
import numpy as np
import pylab as pl
import matplotlib,os
import linecache
import pexpect,time

Port = '2277'
RESOUTLOG = './total_handler.txt'
# Remote host IP address
IpAddress = '172.16.124.70'
# Username for login
LoginName = 'admin'
# Password for login
LoginPassword = 'admin123'
# Prompt such as:’ $ ’ , ‘ # ’ or ’ > ’
LoginPrompt = '#'
TestTimes = '100'
#def fd_check():

def RunCheck():
	os.system('cp fd_check.sh ~/tftpboot\n')
	time.sleep(0.2)
	cmd = 'telnet ' + IpAddress +' '+Port
	telnet = pexpect.spawn(cmd)
	mylist = telnet.expect(["NVR login:"])
	if ( mylist == 0 ):
		telnet.sendline(LoginName)
		mylist2 = telnet.expect(["[pP]assword"])
		telnet.sendline(LoginPassword)
		telnet.expect(LoginPrompt)
		if (mylist2 == 0):
			print 'Telnet to the DUT!!!'
			telnet.sendline('cd /ramdisk\n')
			telnet.expect(LoginPrompt)
			print 'Uploading the fd_check.sh!!!'
			telnet.sendline('tftp 172.16.124.21 -g -r fd_check.sh\n')
			telnet.expect(LoginPrompt)
			telnet.sendline('chmod +x fd_check.sh\n')
			telnet.expect(LoginPrompt)
			print 'Running the fd_check.sh!!!'
			telnet.sendline('./fd_check.sh '+TestTimes+'\n')
			telnet.expect(LoginPrompt)
			temp = int(TestTimes)
			time.sleep(temp * 11)
			print 'Downloading the total_handler.txt!!!'
			telnet.sendline('tftp 172.16.124.21 -p -l total_handler.txt\n')
			telnet.expect(LoginPrompt)
			telnet.sendline('rm fd_check.sh total_handler.txt\n')
			telnet.expect(LoginPrompt)
		else:
			print 'Telnet Failed!!!'
			pass
		telnet.close(force=True)
	else:
		print 'Telnet Failed!!!'
		pass
	telnet.close()
	print 'Move total_handler.txt to current dir!!!'
	os.system('mv ~/tftpboot/total_handler.txt .\n')
	time.sleep(0.2)

def Draw_Pic(srcfile):
	fileHandle = open ( srcfile, 'r' )
	count = len(fileHandle.readlines())
	sstr1 = 'count'#search str
	cou_line = []#str 'count' line number
	cou_num = 0#the value of str 'count' 
	flag = 0 #mark cou_line list number
	for n in range(1,count):
		renum1 =linecache.getline(srcfile,n).find(sstr1)
		if renum1 is not -1:#
			cou_num = cou_num +1
		else:
			pass
#	print 'End cou_num is :',cou_num

	x_xx = []#list to store x1,x2,x3...
	y_xx =[]#list to store y1,y2,y3...

	for n in range(2,count+1):
		#readlines to read_str in stype str
		read_str = linecache.getline(srcfile,n)
		#serach for 'count' and mark 
		renum1 =linecache.getline(srcfile,n).find(sstr1)
		if renum1 is not -1:
			cou_line.append(n)#when find 'count',add the line number to cou_line list
			temp = read_str[read_str.find('count')+7:read_str.find('\n')].strip()
			x_xx.append(temp)
			flag = flag +1
		else:
			y_xx.append(read_str.split())
#	print 'End x_xx is :',x_xx
#	print 'End y_xx is :',y_xx
#	print 'End cou_line is :',cou_line
	fileHandle.close()

	line_type = ['y','m','r','g','b','k','c','--y','--m','--c','--r','--g','--b','--w','--k']
	y_num = len(y_xx) / cou_num
	filenum = []
	filename = []
	for i in range(0,y_num):
		filenum.append('%d' %i)
		filename.append(y_xx[i][1])
		f=open('load'+filenum[i]+'.txt','a')
		for j in range(0,cou_num):
			f.write(x_xx[j]+' '+y_xx[i][0]+'\n')
			i=i+y_num
		f.close()
#	print 'filenum is :',filenum

	for i in range(0,y_num):
		data = 'data'+filenum[i]
		data = np.loadtxt('load'+filenum[i]+'.txt')
		pl.plot(data[:,0], data[:,1], line_type[i])

	pl.title('FD Leak Check')# give plot a title
	pl.xlabel('Log Times')# make axis labels
	pl.ylabel('Handle Numbers')
	pl.xlim(0.0, float(TestTimes)+1)# set axis limits
#	pl.ylim(0.0, 300.)
	pl.legend((filename),loc = 'right', numpoints=1)# make legend
	endtime = time.strftime('%m%d%H%M%S',time.localtime(time.time()))
	#pl.show()# show the plot on the screen
	pl.savefig('./resoult/pic_'+endtime+'.png', format='png')
	print 'Picture is saved as : pic_'+endtime+'.png'

if __name__ == '__main__':
	os.system('rm *.txt\n')
	RunCheck()
	Draw_Pic(RESOUTLOG)
	os._exit(1)