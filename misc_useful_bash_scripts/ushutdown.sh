#!/bin/bash
while [ true ]
do
	if [ $(users | wc -l) -eq 0 ]
	then
		timer=$(($timer+2))
	else
		timer=0
	fi
	if [ $timer -ge 300 ]
	then
		shutdown -h now
	fi
	sleep 2
done
