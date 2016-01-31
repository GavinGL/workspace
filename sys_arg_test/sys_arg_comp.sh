#!/bin/sh
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: sys_cmd_comp.sh
# Description: 
#########################################################################
DATE=/ramdisk/$1.log
cat /proc/sys/kernel/core_pattern >> $DATE
cat /proc/sys/kernel/hostname >> $DATE
cat /proc/sys/kernel/hotplug >> $DATE
cat /proc/sys/kernel/msgmax >> $DATE
cat /proc/sys/kernel/msgmnb >> $DATE
cat /proc/sys/kernel/panic >> $DATE
cat /proc/sys/kernel/panic_on_oops >> $DATE
cat /proc/sys/kernel/shmall >> $DATE
cat /proc/sys/kernel/shmmax >> $DATE
cat /proc/sys/kernel/shmmni >> $DATE
cat /proc/sys/vm/dirty_background_ratio >> $DATE
cat /proc/sys/vm/dirty_ratio >> $DATE
cat /proc/sys/vm/laptop_mode >> $DATE
cat /proc/sys/vm/panic_on_oom >> $DATE
cat /proc/sys/vm/vfs_cache_pressure >> $DATE
cat /proc/version >> /ramdisk/$1_version.log
