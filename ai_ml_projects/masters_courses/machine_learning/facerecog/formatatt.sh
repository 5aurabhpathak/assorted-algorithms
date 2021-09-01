#!/bin/bash
#bash file to form 60% testset and 40% training set out of 'at&t' database into seperate folders
#as required by my program to work
#unzips and organizes
#Author: Saurabh Pathak
cd data
mkdir -p att trainset testset
cd att
rm -rf *
unzip ../att_faces.zip
for x in $(ls -d */)
do
	str=${x%/}
	cd $str
	i=0
	for f in $(ls)
	do
		if [ $i -lt 6 ]
		then
			mv $f ../../trainset/$str$f
			i=$(($i+1))
		else
			mv $f ../../testset/$str$f
		fi
	done
	cd ..
	rm -rf $str
done
mv ../testset .
mv ../trainset .
exit 0
