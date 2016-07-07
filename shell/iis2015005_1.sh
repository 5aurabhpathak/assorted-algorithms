#!/bin/bash
c=$(ls -l | find *.c)
tt=999999999
for x in $c
do
size=$(stat -c "%s"$x)
if [ $size -lt $tt ]
then
	c=$x
fi
done 
cat $c
exit 0
