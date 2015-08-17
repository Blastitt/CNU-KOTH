#!/usr/bin/env python2

import MySQLdb as mdb
import cgi

search = cgi.FieldStorage()

if search.has_key('myteam'):
	myteam = search.getvalue('myteam')
else:
	myteam = " "

if search.has_key('enemyteam'):
	enemyteam = search.getvalue('enemyteam')
else:
	enemyteam = " "

print "Content-Type: text/html\n"
print '''
<html>
	<head>
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

		<!-- Optional theme -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

		<!-- Latest compiled and minified JavaScript -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

		<title>Scoreboard</title>

	</head>

	<body>

		<div class="container">
			<div class="row">
				<div class="col-sm-6">
					<h1>Scoreboard</h1>
				</div>
				<div class="col-sm-6">
					<div align="right" style="padding-top:25px;">
						<form class="form-inline" action="/cgi-bin/scoreboard.cgi" method="get">
							<div class="form-group">
								<input type="text" class="form-control" name="myteam" placeholder="My team...">
							</div>
							<div class="form-group">
								<input type="text" class="form-control" name="enemyteam" placeholder="Enemy team...">
							</div>
							<button type="submit" class="btn btn-primary">
								<span class="glyphicon glyphicon-search"></span>
							</button>
						</form>
					</div>
				</div>
			</div>	
			<table class="table table-striped table-hover">
				<tr>
					<th>Place</th>
					<th>Team</th>
					<th>Points</th>
				</tr>'''


connection = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with connection:

	cur = connection.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT Name, Points FROM ScoreBoard ORDER BY Points DESC")

	rows = cur.fetchall()
	i = 1

	for row in rows:
		if str.lower(myteam) == str.lower(row["Name"]):
			print '				<tr class="info">'
		elif str.lower(enemyteam) == str.lower(row["Name"]):
			print '				<tr class="danger">'
		else:
			print '				<tr>'
		print '''
					<td>#%d</td>
					<td>%s</td>
					<td>%d</td>
				</tr>''' % (i, row["Name"], row["Points"])
		i += 1


	print "		</table>"

if not connection:
	print '''		</table>
			<p align:"center" class="danger">Could not connect to database...</p>'''

print '''	
		</div>
	</body>
</html>	
'''