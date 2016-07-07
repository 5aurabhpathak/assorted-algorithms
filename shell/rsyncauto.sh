#!/bin/bash
rsync -av --progress --delete-after /home/phoenix/Documents/ phoenix@172.17.22.100:Documents/
rsync -av --progress --delete-after /home/phoenix/Downloads/ phoenix@172.17.22.100:Downloads/
rsync -av --progress --delete-after /home/phoenix/src/ phoenix@172.17.22.100:src/
exit 0
