#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: ftp_download.sh
# Description: 
#########################################################################
ftp -nv<<!
open $1
user $2 $3
binary
cd /ramdisk
lcd /home/guolei/test_scripts/sys_arg_test/resoult
prompt off
hash on
get $4.log
get $4_version.log
close
bye
!
