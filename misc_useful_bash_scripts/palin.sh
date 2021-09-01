#!/bin/bash
read x
revx=$(echo $x | rev)
if [ $revx == $x ]
then echo true
else echo false
fi
exit 0
