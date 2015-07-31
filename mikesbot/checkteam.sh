#!/bin/bash
score=0
team="$1"
webpagecontent="$(curl 127.0.0.1/sites)"
echo $webpagecontent | grep $team
if [ $? -eq 0 ]; then
	let score=$score+1
fi
echo "<br>"$team" scored "$score" more points"
