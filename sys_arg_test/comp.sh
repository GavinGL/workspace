#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: comp.sh
# Description: 
#########################################################################
if [ -z "$1" ];then
	echo "arg invalid!"
	echo "example:"
	echo "./comp.sh a5s/his/s2"
else
	diff resoult/base_log/base.log resoult/$1.log -y > resoult/resoult.txt
	temp=$?
	if [ $temp -eq 0 ];then
			echo "****************"
			echo "*Arg Test Pass!*"
			echo "****************"
	elif [ $temp -eq 1 ];then
			echo "****************"
			echo "*Arg Test Fail!*"
			echo "****************"
	elif [ $temp -eq 2 ];then
			echo "****************"
			echo "**Files Error!**"
			echo "****************"
	fi
fi
