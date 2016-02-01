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
import os,time
import multiprocessing

#Test case switch. '1':on ;'0':off
TestTelnet = 1
TestSsh = 0
TestFtp = 0
SshPort = '2277'
# Remote host IP address
IpAddress = '2.1.1.11'
# Username for login
LoginName = 'admin'
# Password for login
LoginPassword = 'kedacomIPC'
# Prompt such as:’ $ ’ , ‘ # ’ or ’ > ’
LoginPrompt = '[$#>]'

def main(num):
	#define thread pool
	threads = []
	#greate thread objects
	if ( TestTelnet == 1 ):
		for i in range(num):
			threads.append(threading.Thread(target=telnet_cmd, args=(IpAddress,LoginPassword)))
#			p = multiprocessing.Process(target = telnet_cmd, args = (IpAddress,LoginPassword))
#			p.start()
#			print 'mythread id is :',p.pid
	if TestSsh is 1:
		for i in range(0,num):
			threads.append(threading.Thread(target=ssh_cmd, args=(IpAddress,LoginPassword)))
	if TestFtp is 1:
		for i in range(0,num):
			threads.append(threading.Thread(target=ftp_cmd, args=(IpAddress,LoginPassword)))
    #start all threads
	for t in range(len(threads)):
		threads[t].start()
    #The main thread waits for all sub thread exits
	for t in range(len(threads)):
		threads[t].join()

def telnet_cmd(IpAddress,LoginPassword):
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
		    # 将 '\n' 的命令结果输出.
#		    print telnet.before
		    # 将 telnet 子程序的执行权交给用户.
#		    telnet.interact()
#		    print 'Left interact mode.'
		# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
		elif (mylist2 == 1):
			global tel_num_eof
			tel_num_eof = tel_num_eof +1
			print "Telnet login failed, due to EOF!!!"
		elif(mylist2 == 2):
			global tel_num_timeout
			tel_num_timeout = tel_num_timeout +1
			print "Telnet login failed, due to TIMEOUT!!!"
		else:
			pass
		telnet.close(force=True)
	# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
	elif (mylist == 1):
		print "Telnet login failed, due to Unknown host!!!"
		os._exit(0)
	elif(mylist == 2):
		global tel_num_eof
		tel_num_eof = tel_num_eof +1
		print "Telnet login failed, due to EOF!!!"
		os._exit(0)
	elif(mylist == 3):
		global tel_num_timeout
		tel_num_timeout = tel_num_timeout +1
		print "Telnet login failed, due to TIMEOUT!!!"
		os._exit(0)
	else:
		print "Telnet login failed, due to Others!!!"
		os._exit(0)
	telnet.close(force=True)

def ssh_cmd(IpAddress,LoginPassword):
	cmd = 'ssh '+LoginName+'@' + IpAddress+' -p '+SshPort
	# 为 ssh 生成 spawn 类子程序
	ssh = pexpect.spawn(cmd)
	# 期待'login'字符串出现，从而接下来可以输入用户名
	mylist = ssh.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT,
		'Are you sure you want to continue connecting (yes/no)?'])
	if (mylist == 3):
		print 'I am in the ????'
		ssh.sendline('yes\n')
	else:
		pass
	# 期待 "[pP]assword" 出现.
	mylist = ssh.expect(["[pP]assword", pexpect.EOF, pexpect.TIMEOUT])
	if ( mylist == 0 ):
		# 匹配 "[pP]assword" 字符串成功，输入密码.
		ssh.sendline(LoginPassword)
		# 期待提示符出现.
		ssh.expect(LoginPrompt)
		if (mylist == 0):
		    # 匹配提示符成功，输入执行命令 '\n'
		    ssh.sendline('\n')
		    # 期待提示符出现.
		    ssh.expect(LoginPrompt)
		    time.sleep(5)
		    # 将 '\n' 的命令结果输出.
#		    print ssh.before
		    # 将 ssh 子程序的执行权交给用户.
#		    ssh.interact()
#		    print 'Left interact mode.'
		# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
		elif (mylist == 1):
			ssh_num_eof = ssh_num_eof +1
			print "Ssh login failed, due to EOF!!!"
		elif(mylist == 2):
			ssh_num_timeout = ssh_num_timeout +1
			print "Ssh login failed, due to TIMEOUT!!!"
		else:
			pass
		ssh.close(force=True)
	# 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
	elif(mylist == 1):
		print "Ssh login failed, due to EOF!!!"
		os._exit(0)
	elif(mylist == 2):
		print "Ssh login failed, due to TIMEOUT!!!"
		os._exit(0)
	else:
		print "Ssh login failed, due to Others!!!"
		os._exit(0)
	ssh.close(force=True)
'''
def ssh_cmd(ip, passwd, cmd):
	ret = -1
	ssh = pexpect.spawn('ssh admin@%s "%s"' % (ip, cmd))
	try:
		i = ssh.expect(['password:', 'Are you sure you want to continue connecting (yes/no)?'], timeout=5)
		if i == 0 :
			ssh.sendline(passwd)
		elif i == 1:
		    ssh.sendline('yes\n')
		    ssh.expect('password: ')
		    ssh.sendline(passwd)
		ssh.sendline(cmd)
		r = ssh.read()
		print r
		ret = 0
	except pexpect.EOF:
		print "EOF"
		ssh.close()
		ret = -1
	except pexpect.TIMEOUT:
		print "TIMEOUT"
		ssh.close()
		ret = -2
	return ret
'''
def show_resoult(num_timeout,num_eof):
	print 'Success times : ',RepeatTimes-num_eof-num_timeout
	print 'Timeout times : ',num_timeout
	print 'EOF     times : ',num_eof
	print '============================='

if __name__ == '__main__':
	try:
		# Repeat times
		RepeatTimes = 10
		tel_num_timeout = 0
		tel_num_eof =0
		ssh_num_timeout = 0
		ssh_num_eof =0
		ftp_num_timeout = 0
		ftp_num_eof =0
		main(RepeatTimes)
#		print "------------------------"
#		print 'process id:', os.getpid()
#		print vip_list
#		print "------------------------"
		if TestTelnet is 1:
			print '============================='
			print '====== Telnet  Resoult ======'
			print 'Success times : ',RepeatTimes-tel_num_eof-tel_num_timeout
			print 'Timeout times : ',tel_num_timeout
			print 'EOF     times : ',tel_num_eof
			print '============================='
#			show_resoult(tel_num_timeout,tel_num_eof)
		if TestSsh is 1:
			print '============================='
			print '======== Ssh Resoult ========'
			print 'Success times : ',RepeatTimes-ssh_num_eof-ssh_num_timeout
			print 'Timeout times : ',ssh_num_timeout
			print 'EOF     times : ',ssh_num_eof
			print '============================='
#			show_resoult(ssh_num_timeout,ssh_num_eof)
		if TestFtp is 1:
			print '============================='
			print '======== Ssh Resoult ========'
			print 'Success times : ',RepeatTimes-ftp_num_eof-ftp_num_timeout
			print 'Timeout times : ',ftp_num_timeout
			print 'EOF     times : ',ftp_num_eof
			print '============================='
#			show_resoult(ssh_num_timeout,ssh_num_eof)
	except Exception, e:
		print str(e)
#		traceback.print_exc()
		os._exit(1)