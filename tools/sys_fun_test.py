#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 * Copyright (c) 2009-~ Guo lei
 *
 * This source code is released for free distribution under the terms of the
 * GNU General Public License
 *
 * Author:       Guo lei<guolei@kedacom.com>
 * Created Time: Sat 30 Jan 2016 11:33:50 AM CST
 * File Name:    sys_fun_test.py
 *
 * Description:  
'''

import pexpect
import threading
import os,sys,time
import multiprocessing

#Test case switch. '1':on ;'0':off
TestTelnet = 1
TestSsh = 1
TestFtp = 1
# Repeat times
GetTimes = sys.argv[1]
RepeatTimes = int(GetTimes)
# Time Interval of starting threads
TimeInterval = 0.2
# Ssh port number
SshPort = '22'
# Remote host IP address
IpAddress = '2.1.1.10'
# Username for login
LoginName = 'admin'
# Password for login
LoginPassword = 'kedacomIPC'
# Prompt such as:’ $ ’ , ‘ # ’ or ’ > ’
LoginPrompt = '[$#>]'
PasswordPrompt = 'admin@'+IpAddress+'\'s password:'

def main(num):
	#define thread pool
	threads = []
	#greate thread objects
	if ( TestTelnet == 1 ):
		for i in range(num):
			threads.append(threading.Thread(target=telnet_cmd, args=(IpAddress,LoginPassword,tel_list)))
	if TestSsh is 1:
		for i in range(0,num):
			threads.append(threading.Thread(target=ssh_cmd, args=(IpAddress,LoginPassword,ssh_list)))
	if TestFtp is 1:
		for i in range(0,num):
			threads.append(threading.Thread(target=ftp_cmd, args=(IpAddress,LoginPassword,ftp_list)))
    #start all threads
	for t in range(len(threads)):
		threads[t].start()
		time.sleep(TimeInterval)
    #The main thread waits for all sub thread exits
	for t in range(len(threads)):
		threads[t].join()

def telnet_cmd(IpAddress,LoginPassword,tel_list):
	cmd = 'telnet ' + IpAddress
	# 为 telnet 生成 spawn 类子程序
	telnet = pexpect.spawn(cmd)
	# 期待'login'字符串出现，从而接下来可以输入用户名
	mylist = telnet.expect(["login", "(?i)Unknown host", pexpect.EOF, pexpect.TIMEOUT])
	if ( mylist == 0 ):
		# 匹配'login'字符串成功，输入用户名.
		telnet.sendline(LoginName)
		# 期待 "[pP]assword" 出现.
		mylist2 = telnet.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
		# 匹配 "[pP]assword" 字符串成功，输入密码.
		telnet.sendline(LoginPassword)
		# 期待提示符出现.
		telnet.expect(LoginPrompt)
		if (mylist2 == 0):
		    # 匹配提示符成功，输入执行命令 '\n'
		    telnet.sendline('\n')
		    # 期待提示符出现.
		    telnet.expect(LoginPrompt)
		    time.sleep(5)
		    tel_list.append(1)
		    print 'Congratulations! telnet login correct!'
		    # 将 '\n' 的命令结果输出.
#		    print telnet.before
		    # 将 telnet 子程序的执行权交给用户.
#		    telnet.interact()
#		    print 'Left interact mode.'
		# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
		elif (mylist2 == 1):
			tel_list.append(2)
			print "Telnet login failed, due to EOF!!!"
		elif(mylist2 == 2):
			tel_list.append(3)
			print "Telnet login failed, due to TIMEOUT!!!"
		else:
			tel_list.append(0)
		telnet.close(force=True)
	# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
	elif (mylist == 1):
		tel_list.append(0)
		print "Telnet login failed, due to Unknown host!!!"
	elif(mylist == 2):
		tel_list.append(2)
		print "Telnet login failed, due to EOF!!!"
	elif(mylist == 3):
		tel_list.append(3)
		print "Telnet login failed, due to TIMEOUT!!!"
	else:
		tel_list.append(0)
		print "Telnet login failed, due to Others!!!"
	telnet.close()

def ssh_cmd(IpAddress,LoginPassword,ssh_list):
	cmd = 'ssh '+LoginName+'@' + IpAddress+' -p '+SshPort
	# 为 ssh 生成 spawn 类子程序
	ssh = pexpect.spawn(cmd)
	# 期待'passwd'字符串出现，从而接下来可以输入密码
	mylist = ssh.expect(['password:','Are you sure you want to continue connecting (yes/no)?',
		pexpect.EOF,pexpect.TIMEOUT],timeout=5)
	if mylist == 0 :
		ssh.sendline(LoginPassword)
		ssh_list.append(1)
		print 'Congratulations! ssh login correct!'
	elif mylist == 1:
		ssh.sendline('yes\n')
		ssh.expect('password: ')
		ssh.sendline(LoginPassword)
		ssh.sendline('\n')
		ssh_list.append(1)
	elif mylist == 2:
		ssh_list.append(2)
		print "Ssh login failed, due to EOF!!!"
	elif mylist == 3:
		ssh_list.append(3)
		print "Ssh login failed, due to TIMEOUT!!!"
	ssh.close()

def ftp_cmd(IpAddress,LoginPassword,ftp_list):
	# 拼凑 ftp 命令
	cmd = 'ftp ' + IpAddress
	# 利用 ftp 命令作为 spawn 类构造函数的参数，生成一个 spawn 类的对象
	ftp = pexpect.spawn(cmd)
	# 期望具有提示输入用户名的字符出现
	mylist = ftp.expect(["(?i)name", "(?i)Unknown host", pexpect.EOF, pexpect.TIMEOUT])
	# 匹配到了 "(?i)name"，表明接下来要输入用户名
	if ( mylist == 0 ):
		# 发送登录用户名 + 换行符给子程序.
		ftp.sendline(LoginName)
		# 期望 "(?i)password" 具有提示输入密码的字符出现.
		mylist = ftp.expect(["(?i)password", pexpect.EOF, pexpect.TIMEOUT])
		ftp.sendline(LoginPassword)
		# 期望登录成功后，提示符 "ftp>" 字符出现.
		mylist = ftp.expect( ['ftp>', 'Login incorrect', 'Service not available',
			pexpect.EOF, pexpect.TIMEOUT])
		# 匹配到了 'ftp>'，登录成功.
		if (mylist == 0):
			ftp_list.append(1)
			print 'Congratulations! ftp login correct!'
			time.sleep(5)
		elif (mylist2 == 1):
			ftp_list.append(2)
			print "Telnet login failed, due to EOF!!!"
		elif(mylist2 == 2):
			ftp_list.append(3)
			print "Telnet login failed, due to TIMEOUT!!!"
		else:
			ftp_list.append(0)
	# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出
	elif mylist == 3 :
		ftp_list.append(2)
		print "ftp login failed, due to EOF!!!"
	elif mylist == 4:
		ftp_list.append(3)
		print "ftp login failed, due to TIMEOUT!!!"
	else:
		ftp_list.append(0)
		print "ftp login failed, due to Others"
	ftp.close()

if __name__ == '__main__':
	try:
		tel_list = [0]
		ssh_list = [0]
		ftp_list = [0]
		main(RepeatTimes)
#		print "------------------------"
#		print 'process id:', os.getpid()
#		print vip_list
#		print "------------------------"
		if TestTelnet is 1:
			print '============================='
			print '====== Telnet  Resoult ======'
			print 'Success times : ',tel_list.count(1)
			print 'Timeout times : ',tel_list.count(3)
			print 'EOF     times : ',tel_list.count(2)
			print '============================='
#			show_resoult(tel_num_timeout,tel_num_eof)
		if TestSsh is 1:
			print '============================='
			print '======== Ssh Resoult ========'
			print 'Success times : ',ssh_list.count(1)
			print 'Timeout times : ',ssh_list.count(3)
			print 'EOF     times : ',ssh_list.count(2)
			print '============================='
#			show_resoult(ssh_num_timeout,ssh_num_eof)
		if TestFtp is 1:
			print '============================='
			print '======== Ssh Resoult ========'
			print 'Success times : ',ftp_list.count(1)
			print 'Timeout times : ',ftp_list.count(3)
			print 'EOF     times : ',ftp_list.count(2)
			print '============================='
#			show_resoult(ssh_num_timeout,ssh_num_eof)
	except Exception, e:
		print str(e)
#		traceback.print_exc()
		os._exit(1)
