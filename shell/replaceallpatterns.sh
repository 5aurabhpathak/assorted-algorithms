#!/bin/bash
for x in $(ls)
do
	if [[ $(cat $x | grep -e '(a > b) ? a : b' > /dev/null && echo true) == "true" ]]
	then
		echo -n changing $x...
		sed -i "s/$1/$2/g" $x
		echo done
	fi
done
exit 0
