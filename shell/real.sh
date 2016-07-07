#!/bin/bash
a=5.66
b=8.67
op=+
c=$(bc <<< $a+$b)
echo $c
exit 0
