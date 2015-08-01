#!/bin/bash
score=0
team="$1"
logpath="/var/www/ctfplatform/log.log"
echo $(date) Check... >> $logpath
# Notice while it's like 5 lines per service, only like 1 line is custom to the
# service. The rest are identical.

# this does a web server check
# it's relatively simple
# change 127.0.0.1/sites with the appropriate site (www.google.com for instance)
# and it will access the site and look for a flag on the page
# not just visibly, on the entire source
ip=127.0.0.1
content="$(curl $ip/sites)"
echo $content | grep $team > /dev/null
if [ $? -eq 0 ]; then
	let score=$score+1
	echo $(date): $team scored for web server $ip >> $logpath
fi

# this is an anonymous FTP server check
# it does a dir listing
# switch the IP with the appropriate one and have
# the attacker make a file with their name as the name
ip=127.0.0.1
content=$(/ftpchk.sh $ip)
echo $content | grep $team > /dev/null
if [ $? -eq 0 ]; then
	let score=$score+1
	echo $(date): $team scored for ftp server $ip >> $logpath
fi
# 

# Easiest of all
# This checks an anonymous samba server
ip=127.0.0.1
content=$(smbclient //$ip/share -c dir -N)
echo $content | grep $team > /dev/null
if [ $? -eq 0 ]; then
        let score=$score+1
	echo $(date): $team scored for samba server $ip >> $logpath
fi
echo $score
