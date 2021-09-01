#!/bin/bash
for x in $(seq 1 255)
do
	echo Scanning host 172.31.1.$x
	nmap -Pn 172.31.1.$x
done
exit 0
