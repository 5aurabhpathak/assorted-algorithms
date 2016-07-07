#!/bin/bash
if [ $(bc <<< "$1<$2") -eq 1 ]
then echo $2 is bigger
else echo $1 is bigger
fi
exit 0
