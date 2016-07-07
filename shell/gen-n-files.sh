#!/bin/bash
if [ $# -ne 1 ]
then
	echo Error: 1 argument needed >&2
	exit 1
elif [[ $1 == *[a-z]* ]]
then
	echo Error: argument must be a number >&2
	exit 1
fi

for x in $(seq $1)
do
	printf "Creating file-%03d.txt\n" $x
	filename=$(printf "file-%03d.txt" $x)
	for i in $(seq $x)
	do
		echo $i >> $filename
	done
done
exit 0
