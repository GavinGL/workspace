#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: ftp_upload.sh
# Description: 
#########################################################################
ftp -nv<<!
open $1
user $2 $3
binary
hash on
cd /ramdisk
lcd /home/guolei/test_scripts/sys_arg_test
prompt
put sys_arg_comp.sh
close
bye
!
