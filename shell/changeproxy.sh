#!/bin/bash
if [ $UID -ne 0 ]
then
	echo You must be root to do that!
	exit 2
fi
if [ $# -eq 1 ]
then
	proxy=iis2015007:9935427381@$1:8080
elif [ $# -eq 2 ] && [ $2 == "-noauth" ]
then
	proxy=$1:8080
elif [ $# -eq 3 ]
then
	proxy=$2:$3@$1
else
	echo usage: changeproxy.sh ip [-noauth]
	exit 1
fi
echo unsetting old proxy
echo -n setting new proxy...
rm /etc/environment
echo "http_proxy=http://$proxy
https_proxy=http://$proxy
ftp_proxy=http://$proxy" > /etc/environment
echo -n reloading environment on all terminals...
for x in $(ls /dev/pts)
do
	if [[ $x != "ptmx" ]]
	then
		/home/phoenix/src/c/ttyecho /dev/pts/$x . /etc/environment
	fi
done
echo successfully set new proxy
echo done
exit 0
