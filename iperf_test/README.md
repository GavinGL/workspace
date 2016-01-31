#iperf auto test

============================================================
Usage:

1.Before you start test,you must set some parameters below.

*******************************************************
****************Iperf Paramiters Settings *************
*******************************************************
TestMod = '-u'						#Set test mode(TCP:'';UDP:'-u')
DevType = 'cli'						#Set DUT type(Server:'ser';Client:'cli')
DstIP = '2.1.1.9'	 				#Set your PC IP
DstIP2 = '2.1.1.10'					#Set DUT IP
TestTime = '5'						#Set test time(sec)
TestSpeed = 100						#Set packages send speed
TestFrameArray =('64','128','256','512','1024','1280','1472')
									#Set test frame list
Dir_Path = './resoult/'				#Set script path

*******************************************************
**************** Serail Paramiters Config *************
*******************************************************
Serail_Com_Port = '/dev/ttyUSB0'			#Set serial port
Serail_Com_Baud_Rate = 38400		#Set baud rate
Serail_Com_Data_Bits = 8			#Set below default
Serail_Com_Parity = 'N'
Serail_Com_Stop_Bits = 1
Serail_Com_Timeout = 1
Serail_Com_Xonxoff = 0
Serail_Com_Rtscts = 0


2.Start test with command "sudo ./myiperf.py".
	We need root permission to open the serial.
