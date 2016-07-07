#!bin/bash
x=$(date +"%H")
case $x in
	[0-9]|1[0-1])
		tput bold; echo Good morning, $(whoami)
		;;
	1[2-7])
		tput bold; echo Good afternoon, $(whoami)
		;;
	1[8-9]|2[0-3])
		tput bold; echo Good evening, $(whoami)
		;;
esac
