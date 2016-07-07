#!/bin/bash
case $2 in
	"/")
		echo $(($1/$3))
		;;
	"*")
		echo $(($1*$3))
		;;
	"+")
		echo $(($1+$3))
		;;
	"-")	
		echo $(($1-$3))
		;;
	*)	
		echo error: unknown operator
		;;
esac
	
