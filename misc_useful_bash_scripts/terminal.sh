#!/bin/bash
devilspie &
terminator -bp desktop -T DesktopConsole --geometry='500x720' &
sleep 2
terminator -bp desktop -T DesktopLogs --geometry='500x300' -e "journalctl -fab" &
exit 0
