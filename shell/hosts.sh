#!/bin/bash
if=$(ifconfig | awk '/<UP,BROADCAST,RUNNING,MULTICAST>/{print substr($1, 1, length($1)-1); exit}')
ipadr=$(ifconfig $if | awk '/inet /{print $2, exit}')
netmask=$(ifconfig $if | awk '/netmask /{print $4, exit}')

#octets
for x in 1 2 3 4
do
	ipoct=$(echo $ipadr | awk -F. '{print $'$x'}')
	suboct=$(echo $netmask | awk -F. '{print $'$x'}')
	if [ $(($ipoct&$suboct)) -ne $ipoct ]
	then
		netid=$(($ipoct&$suboct))
		break
	fi
done

for i in $(seq 0 $(($ipoct-$netid)))
do
	for j in $(seq 0 255)
	do
		host=$(echo $ipadr | awk -F. '{for(k=1;k<'$x';k++) printf "%d.",$k}')$(($netid+$i)).$j
		ping -qc 1 $host 1>/dev/null
		if [ $? -ne 1 ]
		then echo $host is alive
		fi
	done
done
exit 0
