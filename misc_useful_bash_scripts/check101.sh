#!/bin/bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus DISPLAY=:0.0
if [[ $(echo $http_proxy | cut -d. -f4 | cut -d: -f1) -ne 101 ]]
then
	if [[ $(wget --connect-timeout 20 -t 1 --delete-after -e use_proxy=on -e http_proxy=http://172.31.1.101:8080 google.com > /dev/null 2>&1 && echo true || echo false) == "true" ]]
	then
		sudo -u root /home/phoenix/src/shell/changeproxy.sh 172.31.1.101 -noauth
		gsettings set org.gnome.system.proxy.http host 172.31.1.101
		gsettings set org.gnome.system.proxy.http port 8080
		gsettings set org.gnome.system.proxy.http use-authentication false
		gsettings set org.gnome.system.proxy.https host 172.31.1.101
		gsettings set org.gnome.system.proxy.https port 8080
		gsettings set org.gnome.system.proxy.ftp host 172.31.1.101
		gsettings set org.gnome.system.proxy.ftp port 8080
		gsettings set org.gnome.system.proxy mode manual
		for x in $(ls /dev/pts)
		do
			if [[ $x != "ptmx" ]]
			then
				echo freeproxy found open. Proxy environment set. > /dev/pts/$x
			fi
		done
	fi
elif [[ $(wget --connect-timeout 20 -t 1 --delete-after google.com > /dev/null 2>&1 && echo true || echo false) == "false" ]]
then
	sudo -u root /home/phoenix/src/shell/changeproxy.sh 172.31.1.4
	gsettings set org.gnome.system.proxy.http host 172.31.1.4
	gsettings set org.gnome.system.proxy.http port 8080
	gsettings set org.gnome.system.proxy.http use-authentication true
	gsettings set org.gnome.system.proxy.http authentication-user iis2015007
	gsettings set org.gnome.system.proxy.http authentication-password 9935427381
	gsettings set org.gnome.system.proxy.https host 172.31.1.4
	gsettings set org.gnome.system.proxy.https port 8080
	gsettings set org.gnome.system.proxy.ftp host 172.31.1.4
	gsettings set org.gnome.system.proxy.ftp port 8080
	gsettings set org.gnome.system.proxy mode manual
	for x in $(ls /dev/pts)
	do
		if [[ $x != "ptmx" ]]
		then
			echo freeproxy found closed. Proxy environment reset to login proxy. > /dev/pts/$x
		fi
	done
fi
exit 0
