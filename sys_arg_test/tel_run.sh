#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: tel_run.sh
# Description: 
#########################################################################
echo rm -f resoult/*.log
echo rm -f resoult/*.txt
(
sleep 1;echo $3;
sleep 1;echo $4;
sleep 1;echo cd /ramdisk;
sleep 1;echo rm -f *.log
sleep 1;echo chmod +x sys_arg_comp.sh;
sleep 1;echo ./sys_arg_comp.sh $5;
sleep 3;echo exit;
)|telnet $1 $2|cat;
