#! /usr/bin/env python2

import socket
import time


class scorebot():

	def __init__(self, iplist, keylist, outfile, interval):

		self.iplist = open(iplist, 'r')
		self.keylist = open(keylist, 'r')
		self.outfile = open(outfile, 'a')
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

			print("Connecting...")
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.connect((self.status["currentip"], self.status["currentport"]))

			return 1

		except Exception as e:

			print("[!] Error connecting to  %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))
			return 0

	# Get the file sent from the service. Returns 1 on success, 0 on failure
	def getFile(self):
		try:
			print("Requesting File...")
			fileobj = self.connection.makefile('r', 0)
			fileobj.write("GET / HTTP/1.0\n\n")
			self.status["databuffer"] = fileobj.readlines()
			for line in self.status["databuffer"]:
				print(line)
			return 1

		except Exception as e:

			print("[!] Error getting banner of %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))
			return 0

	# Parse databuffer for a key. Returns first Key found, or 0 for none.
	def findKey(self):

		for key in self.keylist:

			if key[0] != '#':

				key = key.split(":")
				self.status["currentkey"] = key[0]
				self.status["currentteam"] = key[1]

				if "".join(self.status["databuffer"]).find(self.status["currentkey"]) != -1:

					self.status["databuffer"] = ""
					return 1


		self.status["databuffer"] = ""
		return 0

	# Connect to each service, get its banner, parse it for a key, appends current time, team name, and points to output file.
	def score(self):

		for line in self.iplist:

			if line[0] != '#':

				line = line.split(":")
				self.status["currentip"] = line[0]
				self.status["currentport"] = int(line[1])
				self.status["pointsworth"] = int(line[2])


				self.status["connected"] = self.connect()

				if self.status["connected"]:

					if self.getFile():

						if self.findKey():

							print("[+] %s scored %d points!" % (self.status["currentteam"], self.status["pointsworth"]))
							currtime = time.strftime("%Y-%m-%d %H:%M:%S")
							self.outfile.write("[%s] %s: + %d\n" % (currtime, self.status["currentteam"], self.status["pointsworth"]))

						self.keylist.seek(0)
						
					self.connection.close()
					self.status["connected"] = False

		self.iplist.seek(0)

if __name__ == '__main__':
	
	myscorebot = scorebot("./config/iplist.cfg", "./config/keylist.cfg", "./output/scorelog.txt", 10)

	while True:

		myscorebot.score()
		time.sleep(myscorebot.interval)