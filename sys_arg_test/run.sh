#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: run.sh
# Description: 
#########################################################################
clear
ping -c 4 $1
if [ $? -eq 0 ];then
	if [ -n "$1" ]&&[ -n "$2" ]&&[ -n "$3" ]&&[ -n "$4" ]&&[ -n "$5" ];then
		./ftp_upload.sh $1 $3 $4 $5
		./tel_run.sh $1 $2 $3 $4 $5
		./ftp_download.sh $1 $3 $4 $5
		./comp.sh $5
		./report_in_order.sh $5
        cd resoult
        ls
	else
		echo "Args Invalid!"
		echo "Example:"
		echo "./run.sh 172.16.124.75 23  admin kedacomIPC a5s/his/s2"
		echo "./run.sh 172.16.124.71 2277  admin admin123 his"
	fi
else
	echo "The IP is not alive!"
	echo "Example:"
	echo "./run.sh 172.16.124.75 23  admin kedacomIPC a5s/his/s2"
	echo "./run.sh 172.16.124.71 2277  admin admin123 his"
fi
