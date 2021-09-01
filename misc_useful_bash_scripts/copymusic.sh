#!/bin/bash
if [ $UID -ne 0 ]
then echo You need to be root to do that!
	exit 1
fi
umount /dev/sda3
mount -o rw /dev/sda3 /media/winc
echo -n copying all music to Music library...
mv /home/phoenix/Music/*.* /media/winc/Users/Saurabh/Music 2>/dev/null
sleep 3
umount /dev/sda3
mount /dev/sda3
echo done!
exit 0
