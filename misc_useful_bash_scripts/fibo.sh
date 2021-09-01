#!/bin/bash
read x
first=0
second=1
fib()	{
	if [ $1 -gt 1 ]
	then
		sum=$(($first+$second))
		first=$second
		second=$sum
		echo -n "$sum "
		fib $(($1-1))
	fi
}

echo -n "0 1 "
fib $x
echo
exit 0
	
