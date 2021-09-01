#!/bin/bash
cd ~/src/shell/examples
for x in $(seq 0 23)
do
	if [ $x -lt 10 ]
	then
		curl -O https://iws44.iiita.ac.in/bss/website/courses/pg/aap-2015/scripts/aap_shell_0$x.sh
	else
		curl -O https://iws44.iiita.ac.in/bss/website/courses/pg/aap-2015/scripts/app_shell_$x.sh
	fi
done
exit 0
