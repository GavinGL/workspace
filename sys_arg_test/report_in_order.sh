#!/bin/bash
#########################################################################
# Copyright (c) 2009-~ Guo lei
# 
# This source code is released for free distribution under the terms of the
# GNU General Public License
# 
# Author:    Guo lei<guolei@kedacom.com>
# File Name: put_in_order.sh
# Description: 
#########################################################################
touch resoult/temp1.txt
rm -f resoult/$1_test_report.txt 
touch resoult/$1_test_report.txt 
sed '1d' resoult/$1_test_report.txt resoult/$1_test_report.txt
echo "*********************************************************************************" >> resoult/$1_test_report.txt
echo "*********Args***********************Reference********************Actual**********" >> resoult/$1_test_report.txt
echo "*********************************************************************************" >> resoult/$1_test_report.txt

awk '{print $1}' resoult/base_log/base.log | paste -  resoult/$1.log >> resoult/temp1.txt
awk '{print $1}' arg_base.txt | paste -  resoult/temp1.txt >> resoult/$1_test_report.txt
echo >> resoult/$1_test_report.txt
echo >> resoult/$1_test_report.txt
echo "**********************************************************************************" >> resoult/$1_test_report.txt
echo "*********************************Parameter comparison*****************************" >> resoult/$1_test_report.txt
echo "********Reference******************************************Actual*****************" >> resoult/$1_test_report.txt
cat resoult/resoult.txt >> resoult/$1_test_report.txt
echo >> resoult/$1_test_report.txt
echo >> resoult/$1_test_report.txt
echo "**********************************************************************************" >> resoult/$1_test_report.txt
echo "************************************Device  Version*******************************" >> resoult/$1_test_report.txt
echo "**********************************************************************************" >> resoult/$1_test_report.txt
cat resoult/$1_version.log >> resoult/$1_test_report.txt
rm -f resoult/temp1.txt
rm -f resoult/resoult.txt
rm -f resoult/$1_version.log
