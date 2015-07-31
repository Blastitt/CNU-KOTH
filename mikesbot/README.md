This is a work in progress. I'll push routinely. Also don't judge the front-end. That comes last, if at all.


dbauth.php would house MySQL credentials.


*	 installation: apt-get install lamp-server^

*	 move checkteams.sh to / of the filesystem or edit code for custom location

*	 add the following cron job, optionally changing the auth token

(a ton of *s depending on scoring interval, for every minute it's just 5 *s)	root	curl localhost/ctfplatform/score.php?token=dd662924a075309a141ef0ae2bd46daa

