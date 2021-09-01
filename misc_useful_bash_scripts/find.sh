#!/bin/bash
for x in $(ls -R)
do
	if [[ $x == *.sh ]]
	then	echo $x
	fi
done
exit 0
