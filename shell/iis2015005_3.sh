#!/bin/bash
declare -a arr
read x
for (( i=0;i<$x;i++ ))
	do
	read arr[$i]
done
flag=0
for (( j=0;j<$x;j++ ))
do
	if [ $j -eq 0 ]
	then 
	temp=$(echo $arr[$j]| rev)
	r=$(($temp/10))
	r=$(($temp%10))
	fi
	temp=$(echo $arr[$j]| rev)
	oo=$(($temp/10))
	oo=$(($temp%10))
	if [ $oo == $r ]
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

