#!/bin/bash
while getopts :cd opt
do
	case $opt in
	c)
		clear;;
	d)
		pwd;;
	?)
		echo invalid argument;;
	esac
done
exit 0
