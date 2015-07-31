This is a work in process. I'll push routinely. Also don't judge the front-end. That comes last, if at all.


dbauth.php would house MySQL credentials.


** installation: apt-get install lamp-server^
** move checkteams.sh to / of the filesystem or edit code for custom location
** add the following cron job, optionally changing the auth token
* * * * 	root	curl localhost/ctfplatform/score.php?token=dd662924a075309a141ef0ae2bd46daa

