#!/bin/bash

if [ "$#" -ne "1" ]; then
	echo "Usage: $0 inspector_ip"
	exit 1
fi

INSPECTOR_IP=$1

DISK_SIZE=`snmpwalk -Oqv -u snmpuser -A "HivY%>zd12Fdd" -a SHA -x AES -X "opKJ8&9@>qwzd" -lauthPriv ${INSPECTOR_IP} .1.3.6.1.4.1.2021.9.1.6`
DISK_FREE=`snmpwalk -Oqv -u snmpuser -A "HivY%>zd12Fdd" -a SHA -x AES -X "opKJ8&9@>qwzd" -lauthPriv ${INSPECTOR_IP} .1.3.6.1.4.1.2021.9.1.7`

#echo ${DISK_SIZE}
#echo ${DISK_FREE}

DISK_TOTAL_SIZE=0
for disk_size in ${DISK_SIZE}
do
	DISK_TOTAL_SIZE=$((DISK_TOTAL_SIZE + $disk_size))
done
#echo ${DISK_TOTAL_SIZE}

DISK_TOTAL_FREE=0
for disk_free in ${DISK_FREE}
do
	DISK_TOTAL_FREE=$((DISK_TOTAL_FREE + $disk_free))
done
#echo ${DISK_TOTAL_FREE}

DISK_USAGE_PERCENT=$(((DISK_TOTAL_SIZE - DISK_TOTAL_FREE) * 100 / DISK_TOTAL_SIZE))
echo "Disk usage of inspector: ${DISK_USAGE_PERCENT}%"

exit 0

