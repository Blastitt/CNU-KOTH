gucci="1"

# Service check with ftp
/ftpchk.sh 127.0.0.1 | grep "Not connected"
if [ $? -eq 0 ]; then
	gucci="0"
fi

# Service check with curl
curl 127.0.0.1/sites > /dev/null
if [ $? -ne 0 ]; then
	gucci="0"
fi

# Service check with samba
smbclient //127.0.0.1/share -c dir -N > /dev/null
if [ $? -ne 0 ]; then
	gucci="0"
fi

#Dont remove this
echo $gucci
