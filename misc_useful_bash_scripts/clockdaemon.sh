#!/bin/bash
oldcolumns=$(tput cols)
while [ true ]
do
	columns=$(tput cols)
	tput sc
	if [ $columns -ne $oldcolumns ]
	then
		tput cup 0 $(($oldcolumns-11))
		tput el
	fi
	tput cup 0 $(($columns-11))
	date +"%r"
	oldcolumns=$columns
	tput rc
	sleep 1
done
