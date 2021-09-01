#!/bin/bash
row=1
column=1
for ((i=1 ; i<=10; i++))
do
	if [ $column -gt $row ]
	then
		row=$(($row+1))
		column=1
		echo
	fi
	echo -n "$i "
	column=$(($column+1))
done
echo
exit 0
