#!/usr/bin/env python2

import MySQLdb as mdb

import warnings
warnings.filterwarnings("ignore")


class dbpopulator():
	def __init__(self, dbconfig, teamlist):

		self.dbuser = None
		self.dbpass = None
		self.db = None
		self.dbip = None
		self.connection = None
		self.teams = None
		self.dbconfig = open(dbconfig, 'r')
		self.teamlist = open(teamlist, 'r')

	def dbconnect(self):

		settings = self.dbconfig.readlines()
		self.dbconfig.close()

		for line in settings:
			line = line.split('=')

			if line[0] == "user":
				self.dbuser = line[1].strip('\n')
			elif line[0] == "pass":
				self.dbpass = line[1].strip('\n')
			elif line[0] == "database":
				self.db = line[1].strip('\n')
			elif line[0] == "ip":
				self.dbip = line[1].strip('\n')

		self.connection = mdb.connect(self.dbip, self.dbuser, self.dbpass, self.db, connect_timeout=5)

	def getteams(self):

		self.teams = self.teamlist.readlines()
		self.teamlist.close()

	def populate(self):

		cur = self.connection.cursor()

		cur.execute("CREATE TABLE IF NOT EXISTS ScoreBoard (Name VARCHAR(10) NOT NULL UNIQUE, Flag VARCHAR(20) NOT NULL UNIQUE, Points INT)")

		for line in self.teams:

			if line[0] != '#' and line[0] != '\n':

				line = line.split(":")
				flag = line[0]
				teamname = line[1].strip('\n')

				cur.execute("INSERT IGNORE INTO ScoreBoard (Flag, Name, Points) VALUES (%s, %s, 0)", (flag, teamname))
				self.connection.commit()

		print("[+] Successfully enrolled new teams into the ScoreBoard table of the database.")
		self.connection.close()

def main():

	mypopulator = dbpopulator("../config/database.cfg", "../config/keylist.cfg")

	mypopulator.dbconnect()
	mypopulator.getteams()
	mypopulator.populate()