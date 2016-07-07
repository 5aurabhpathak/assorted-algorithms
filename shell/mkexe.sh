#!/bin/bash
find ~/src/shell/* ! -perm 774 -exec chmod 774 {} \;
exit 0
