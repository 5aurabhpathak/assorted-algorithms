#!/bin/bash
for x in $(seq 254); do
    ping -c1 -w2 172.18.0.$x >/dev/null 2>&1
    echo 172.18.0.$x >> ~/Documents/alivehosts.txt
  if [ $? -eq 0 ]; then
      x=$(sudo nmap -Pn -p 135,139,445 --script samba-vuln-cve-2012-1182,smb-check-vulns,smb-enum-sessions,smb-enum-users --script-args smbbasic=1,unsafe=1 172.18.0.$x)
      if [[ $(echo $x | grep -iw open >/dev/null && echo true || echo false) == "true" ]]; then
	echo "172.18.0.$x" >> ~/Documents/intrestinghosts.txt
	echo "$x" >> ~/Documents/intrestinghosts.txt
	echo ""
     fi
     echo "$x"
     echo ""
  fi
done
exit 0
