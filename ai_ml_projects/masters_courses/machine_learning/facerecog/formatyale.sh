#!/bin/bash
#bash file to form 60% testset and 40% training set out of 'yalefaces' database into seperate folders as required by my program to work
#unzips and organizes
#Author: Saurabh Pathak
cd data
rm -rf yalefaces 2>/dev/null
mkdir -p testset trainset
unzip yalefaces.zip 'yalefaces/*'
cd yalefaces
declare -A aa
for x in $(ls -1)
do
	if [[ $x == 'Readme.txt' ]]
	then continue
	fi
	subject=${x%.*}
	if [[ -z ${aa[$subject]} ]]
	then aa[$subject]=0
	fi
	if [ ${aa[$subject]} -lt 7 ]
	then
		aa[$subject]=$((${aa[$subject]}+1))
		mv $x ../trainset/
	else mv $x ../testset/
	fi
done
mv ../testset .
mv ../trainset .
exit 0
