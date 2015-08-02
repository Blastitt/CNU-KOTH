#!/bin/bash
ftp -n $1 <<END_SCRIPT
quote USER anonymous
quote PASS lolpwn
dir
quit
END_SCRIPT

