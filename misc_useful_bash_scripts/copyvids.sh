#!/bin/bash
if [ $UID -ne 0 ]
then echo You need to be root to do that!
	exit 1
fi
if [ $# -ne 2 ]
then echo Usage: copyvid.sh <dirname> <relative location in video library>
	exit 2
fi
umount /dev/sda3
mount -o rw /dev/sda3 /media/winc
cd $1
mkdir -p /media/winc/Users/Saurabh/Videos/$2
echo -n copying all videos in $1 to video library...
mv *.mp4 /media/winc/Users/Saurabh/Videos/$2/
mv *.flv /media/winc/Users/Saurabh/Videos/$2/
mv *.avi /media/winc/Users/Saurabh/Videos/$2/
mv *.mkv /media/winc/Users/Saurabh/Videos/$2/
umount /dev/sda3
mount /dev/sda3
echo done!
exit 0
