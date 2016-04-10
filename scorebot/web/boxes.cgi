#!/usr/bin/env python2

import MySQLdb as mdb
import cgi

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

		<title>Boxes</title>

	</head>

	<body>

		<div class="container">
			<div class="row">
				<div class="col-sm-6">
					<h1>Boxes</h1>
				</div>
				<div class="col-sm-6">
					<div align="right" style="padding-top:25px;">
					</div>
				</div>
			</div>	
			<table class="table table-striped table-hover">
				<tr>
					<th>Box</th>
					<th>Points</th>
					<th>Owned By</th>
				</tr>'''


connection = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with connection:

	cur = connection.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT IP, Points, OwnedBy FROM Boxes ORDER BY Points DESC")

	rows = cur.fetchall()
	i = 1

	for row in rows:
		print '				<tr>'
		print '''
					<td>#%d</td>
					<td>%s</td>
					<td>%d</td>
					<td>%s</td>
				</tr>''' % (i, row["IP"], row["Points"], row["OwnedBy"])
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
