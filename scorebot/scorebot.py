#! /usr/bin/env python2

import socket # Connecting to services
import time   # Waiting the specified interval
import thread # Doing multiple things at once


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
			"currentproto" : None,
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
			self.connection.connect((self.status["currentip"], self.status["currentport"]))

			return 1

		except Exception as e:

			print("[!] Error connecting to  %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))
			return 0

	# Get the index.html from the HTTP service.
	def getHTTP(self):

		try:

			fileobj = self.connection.makefile('r', 0)
			fileobj.write("GET / HTTP/1.0\n\n")
			self.status["databuffer"] = fileobj.readlines()

		except Exception as e:

			print("[!] Error getting file from %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))

	# Get the FTP banner.
	def getFTP(self):

		try:

			self.connection.sendall("HELP\r\n")
			self.status["databuffer"] = self.connection.recv(1024)

		except Exception as e:

			print("[!] Error getting FTP banner from %s:%d - %s" % (self.status["currentip"], self.status["currentport"], str(e)))


	# Parse databuffer for a key and give the team points if their key is found.
	def findKeys(self):

		for key in self.keylist:

			if key[0] != '#':

				key = key.split(":")
				self.status["currentkey"] = key[0]
				self.status["currentteam"] = key[1].strip("\n")

				if "".join(self.status["databuffer"]).find(self.status["currentkey"]) != -1:
					
					print("[+] %s scored %d points!" % (self.status["currentteam"], self.status["pointsworth"]))
					currtime = time.strftime("%Y-%m-%d %H:%M:%S")
					self.outfile.write("[%s] %s: + %d\n" % (currtime, self.status["currentteam"], self.status["pointsworth"]))
					
					self.status["databuffer"] = ""


		self.status["databuffer"] = ""
		self.keylist.seek(0)


	# Connects to each service and scores it.
	def score(self):

		for line in self.iplist:

			if stop:
				break

			if line[0] != '#':

				line = line.split(":")
				self.status["currentproto"] = str.upper(line[0])
				self.status["currentip"] = line[1]
				self.status["currentport"] = int(line[2])
				self.status["pointsworth"] = int(line[3])


				self.status["connected"] = self.connect()

				if self.status["connected"]:

					if self.status["currentproto"] == "HTTP":

						self.getHTTP()

					elif self.status["currentproto"] == "FTP":

						self.getFTP()
					
					else:

						print("[!] The %s protocol is not currently supported." % self.status["currentproto"])

					self.findKeys()

					self.connection.close()
					self.status["connected"] = False


		self.iplist.seek(0)


if __name__ == '__main__':
	
	# We're gonna thread this so the user can stop the loop at any time.
	def interrupt(stop):

		raw_input("\nPress ENTER to stop scoring.\n\n")
		stop.append(None)

	# So runs with longer intervals don't have to wait too long between hitting ENTER and actually stopping.
	def waitInterval(interval):

		interval = interval / 5

		i = 0

		while i < 5:

			if stop:
				break

			time.sleep(interval)
			i += 1



	myscorebot = scorebot("./config/iplist.cfg", "./config/keylist.cfg", "./output/scorelog.txt", 10)

	stop = []

	# Just some hacky stuff to make the loop stop when you hit ENTER
	thread.start_new_thread(interrupt, (stop,))

	while True:

		myscorebot.score()
		if stop:
			break
		waitInterval(myscorebot.interval)


	myscorebot.iplist.close()
	myscorebot.keylist.close()
	myscorebot.outfile.close()
