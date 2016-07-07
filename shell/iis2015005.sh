#!/bin/bash
read x
declare -a arr
for (( i=0;i<$x;i++ ))
do
read arr[$i]
flag=0;
done
for (( j=0;j<$x;j++ ))
do
if [ ${arr[$j]} == ${arr[$x-1-$j]} ]
then
flag=0 
else
flag=1
fi
done
if [ $flag -eq 1 ]
then 
echo no
else 
echo yes
fi

