#!/bin/sh 
set -x 
echo "	Num		PID" > total_handler.txt 
#echo "max_handler is:" 
#ulimit -n >> total_handler.txt

psid=`ps -ef|grep $1|head -1|awk '{print $2}'` 
count=0 
while [ $count -lt $1 ] 
do 
	echo "count = " $count >> total_handler.txt
	lsof -n|awk '{print $2}'|sort|uniq -c|sort -nr >> total_handler.txt
#	lsof -p $psid|wc -l >> total_handler 
	sleep 10 
	count=`expr $count + 1` 
done 
