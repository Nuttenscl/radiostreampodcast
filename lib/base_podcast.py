from prettytable import PrettyTable
import feedparser
import subprocess 
import sqlite3

def connecttodb():
		conn = sqlite3.connect('podcast.db')
		return conn

class emission:
	def __init__(self,name,podcasturl="",podcastid=0):
		self.name=name
		self.podurl=podcasturl
		self.podid = podcastid
	#def listpodcasts(self):
		#print "None to show"
	def listpodcasts(self,number=7,all=False):
		try:
			d = feedparser.parse(self.podurl) 
		except SAXException:
			parser.error("error")
			return 0
		if all:
			a=len(d['entries'])
		else:
			a=number
		x = PrettyTable(["id","Title", "date","url"])
		x.align["Title"] = "l" # Left align 
		x.align["date"] = "l" # Left align 
		x.align["url"] = "l" # Left align
		x.padding_width = 1 # One space between column edges and contents (default)
		print "Programme: "+d['channel']['title']
		print "Author: "+d['channel']['author']
		print "podcast xml: "+d['channel']['summary_detail']['base']
		for ii,e in zip(range(len(d['entries'])),d['entries'][:a]):
			x.add_row([ ii, e['title'],e['updated'], e['id'] ])
		print x

	def playpodcast(self,Tid):
		d = feedparser.parse(self.podurl) 
		urltoplay = str(d['entries'][Tid]["id"])
		print "mplayer %s" % urltoplay
		subprocess.call(["mplayer",urltoplay])

	def __str__(self):
		out="nom:\t\t"+self.name+"\npodurl:\t"+self.podurl+"\npodcast id:\t"+self.podid
		return out

class station:
	def __init__(self,name,code="",url="",streamurl="",lso=False,query=False):
		self.name=name
		self.code=code
		self.url=url
		self.streamurl=streamurl
		self.query=query
		self.lso=lso
		#self.__listemission()	

	def __str__(self):
		out="nom:\t\t"+self.name+"\nbase url:\t"+self.url
		return out

	def fillemission(self):
		emissions=[]
		self.emissions=emissions
	#__listemission = listemission

	def playstation(self):
		urltoplay=self.streamurl
		subprocess.call(["mplayer","-cache-min","2",urltoplay])

	def listemissions(self,query=""):
		if not hasattr(self,"emissions") or not query=="" or self.emissions==[]:
			self.fillemission(query)
		x = PrettyTable(["index","Title", "id"])
		x.align["Title"] = "l" # Left align 
		x.align["id"] = "l" # Left align
		x.padding_width = 1 # One space between column edges and contents (default)
		for e,ii in zip(self.emissions,range(len(self.emissions))):
			x.add_row([ii,e.name, e.podid ])
		print x

	def listemissionsfromdb(self,query=""):
		conn = sqlite3.connect('db/podcast.db')
		c = conn.cursor()
		ql="select * from emissions where station=='"+self.name+"'"
		x = PrettyTable(["id","Title", "localid"])
		x.align["Title"] = "l" # Left align 
		x.align["id"] = "l" # Left align
		x.padding_width = 1 # One space between column edges and contents (default)
		for row in conn.execute(ql):
			x.add_row([row[0], row[2],row[4] ])
		conn.close()
		print x


	def cleardb(self):
		#conn = sqlite3.connect('podcast.db')
		conn = connecttodb()
		c = conn.cursor()
		qd="delete from emissions where station=='"+self.name+"'"
		print qd
		c.execute(qd)
		conn.commit()
		conn.close()

class stationgroup:
	def __init__(self,name,stations=[]):
		self.name=name
		self.stations=stations
