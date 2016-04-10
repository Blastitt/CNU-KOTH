# CNU-KOTH
Ethical hacking King of the Hill competition at CNU

## Scorebot
### Basic Setup
1. Fill out the configuration files found in the /config/ directory.
2. Place the contents of the /web/ directory into your web server's directory and make them executable. You may have to configure your web server to allow execution of CGIs.
3. Run runme.py in the /scripts/ directory. This will enroll the teams configured in keylist.cfg into your MySQL database and stage the boxes in iplist.cfg for scoring. Scoring should start automatically.

### Custom Flag Files
You may want to have your teams plant their flags in custom files on your vulnerable servers. The way we implemented this in our last competition was the following:

1. Make the custom file, e.g. flag.txt
2. Run an ncat listener that serves the contents of flag.txt, e.g. ncat -lkp 1738 -e "/bin/cat /path/to/flag.txt"
3. Insert a custom entry into your iplist.cfg file, e.g. CUST:192.168.1.27:1738:2000

The scorebot will connect to port 1738 on 192.168.1.27 and receive the contents of flag.txt to parse for flags.

To stop the scorebot properly, hit the ENTER key (CTRL-C if it hangs for too long).

### Web Front End
#### scoreboard.cgi
Real-time scoreboard. Must be refreshed to update.

#### boxes.cgi
Shows IP and point value of scored boxes, as well as the last team to successfully plant their flag in each. Boxes added to iplist.cfg after scoring is started will not show up on this page. To see such boxes, runme.py must be restarted.
