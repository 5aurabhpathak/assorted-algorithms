#!/bin/bash

a=$(bc <<< 0123)

while [ $a -ne 0 ] 
do
	a=$(($a/10))
	echo "$a hi"
done
