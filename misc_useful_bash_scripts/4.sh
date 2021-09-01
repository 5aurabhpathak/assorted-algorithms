#!/bin/bash
#This will print the biggest out of any number of arguments
if [ $# -eq 0 ]
then
	echo Error: no arguments
else
	big=0
	for x in $@
	do
		if [ $big -lt $x ]
		then
			big=$x
		fi
	done
	echo $big
fi
exit 0
