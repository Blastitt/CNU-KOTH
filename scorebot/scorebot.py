#! /usr/bin/env python2

import socket
import time


class scorebot(Object):

	def __init__(self, iplist, keylist, outfile, interval):

		self.iplist = open(iplist, 'r')
		self.keylist = open(keylist, 'r')
		self.outfile = open(outfile, "r+")
#		self.sqladdr = sqladdr		Maybe add SQL database functionality later.
		self.interval = interval
		self.connection = None

		self.status = {
			"connected" : False,
			"databuffer" : "",
			"currentip" : None,
			"currentport" : None,
			"currentkey" : None,
			"currentteam" : None,
			"pointsworth" : 0
		}

	# Connect to a service. Returns 1 on success, 0 on failure.
	def connect(self):
		try:

			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.connect(self.status["currentip"], self.status["currentport"])

			return 1

		except Exception as e:

			print("[!] Error connecting to  %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))
			return 0

	# Get the first 1024 bytes sent from the service. Returns 1 on success, 0 on failure
	def getBanner(self):
		try:

			self.status["databuffer"] = self.connection.recv(1024)
			return 1

		except Exception as e:

			print("[!] Error getting banner of %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))
			return 0

	# Parse databuffer for a key. Returns first Key found, or 0 for none.
	def findKey(self):

		for key in keylist:

			if key[0] != '#':

				key = key.split(":")
				self.status["currentkey"] = key[0]
				self.status["currentteam"] = key[1]

				if self.status["databuffer"].find(self.status["currentkey"]) != -1:

					self.status["databuffer"] = ""
					return 1


		self.status["databuffer"] = ""
		return 0

	# Connect to each service, get its banner, parse it for a key, appends current time, team name, and points to output file.
	def score(self):

		for line in iplist:

			if line[0] != '#':

				line = line.split(":")
				self.status["currentip"] = line[0]
				self.status["currentport"] = int(line[1])
				self.status["pointsworth"] = int(line[2])


				self.status["connected"] = self.connect()

				if self.status["connected"]:

					if self.getBanner():

						if self.findKey():

							currtime = time.strftime("%Y-%m-%d %H:%M:%S")
							self.outfile.append("[%s] %s: + %d\n" % (currtime, self.status["currentteam"], self.status["pointsworth"]))

					self.connection.close()
					self.status["connected"] = False

if __name__ == '__main__':
	
	myscorebot = scorebot("./config/iplist.cfg", "./config/keylist.cfg", "./output/scorelog.txt", 60)

	while True:

		myscorebot.score()
		time.sleep(myscorebot.interval)