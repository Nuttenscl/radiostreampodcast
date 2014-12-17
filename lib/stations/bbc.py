import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
import subprocess 
from lib.base_podcast import emission, station, stationgroup
from prettytable import PrettyTable
import sqlite3

class stationbbc(station):
	def __init__(self,name,code,nomcode="",streamurl="",titlearg="",urlarg=""):
		podurlcomp= "http://www.bbc.co.uk/podcasts/"+nomcode+"/a-z"
		station.__init__(self,name,code,podurlcomp,streamurl)
		self.name=name
		self.code=code
		self.url=podurlcomp
		self.nomcode=nomcode
		self.streamurl=streamurl
		self.argtitle=titlearg
		self.argurl=urlarg
		self.emissions=[]

	def fillemission(self,query="",iditt=1):
		emissions=[]
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		if iditt==1:
			page= html.parse(self.url)
		else:
			page= html.parse(self.url+"?page="+str(iditt)+"#results-list")
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
			expressionurl = GenericTranslator().css_to_xpath(self.argurl)
			expressionother = GenericTranslator().css_to_xpath(".nav-pages a")
		except SelectorError:
			return 0
			#feedparser.error('Invalid CSS selector')
	
		for e,eid in zip(page.xpath(expressiontitle),page.xpath(expressionurl)):
			if eid.get("href"):
				try:
					found =re.search('.*/([^/]*)$', eid.get("href")).group(1)
				except AttributeError:
					found = '' 
			else:
				found=""
			etemp = emissionbbc(e.text,found,self.nomcode)
			emissions.append(etemp)
		
		for eoth in page.xpath(expressionother):
			totest=self.url+"?page="+str(iditt+1)+"#results-list"
			if eoth.get("href")==totest:
				print "yes "+eoth.get("href")
				self.fillemission(query,iditt+1)
				break
		if iditt==11:
			self.emissions=emissions
		else :
			self.emissions+=emissions

	def fillemissionindb(self,query=""):
		self.cleardb()
		conn = connecttodb()
		c = conn.cursor()
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		page= html.parse(self.url)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
			expressionurl = GenericTranslator().css_to_xpath(self.argurl)
		except SelectorError:
			return 0
			#feedparser.error('Invalid CSS selector')
	
		for e,eid in zip(page.xpath(expressiontitle),page.xpath(expressionurl)):
			if eid.get("href"):
				try:
					if self.name=="France culture":
						foundb =re.search('/podcast/(.*)', eid.get("href")).group(1)
						pageb = html.parse("http://www.franceculture.fr/podcast/"+foundb) 
						aaa= pageb.xpath(GenericTranslator().css_to_xpath(".lien-rss"))[0]
						found = re.search("http.*rss_(.*)\.xml",aaa.get("href")).group(1)
						print found
					else:
						found =re.search('http.*rss_(.*)\.xml', eid.get("href")).group(1)
				except AttributeError:
				    found = '' 
			else:
				found=""
			etemp = emissionradiofrance(e.text,found)
			qqq = "INSERT INTO emissions (station, title, podcasturl, idemission) VALUES (\""+self.name+"\",\""+etemp.name+"\",'"+etemp.podcasturl+"','"+str(etemp.idpod)+"')"
			print qqq
			c.execute(qqq)
		conn.commit()
		conn.close()

class emissionbbc(emission):
	def __init__(self,name,idpod,nomcode):
		podcasturl="http://downloads.bbc.co.uk/podcasts/"+nomcode+"/"+str(idpod)+"/rss.xml"
		emission.__init__(self,name,podcasturl,idpod)
		self.idpod=idpod
		self.name=name
		self.podcasturl=podcasturl

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
		x = PrettyTable(["id","Titre", "date","url"])
		x.align["Titre"] = "l" # Left align 
		x.align["date"] = "l" # Left align 
		x.align["url"] = "l" # Left align
		x.padding_width = 1 # One space between column edges and contents (default)
		print "Emission: "+d['channel']['title']
		print "Auteur: "+d['channel']['author']
		print "podcast xml: "+d['channel']['summary_detail']['base']
		for ii,e in zip(range(len(d['entries'])),d['entries'][:a]):
			x.add_row([ ii, e['title'],e['updated'], e['link'] ])
		print x

	def playpodcast(self,Tid):
		d = feedparser.parse(self.podurl) 
		urltoplay = str(d['entries'][Tid]["link"])
		print "mplayer %s" % urltoplay
		subprocess.call(["mplayer",urltoplay])


bbc1 = stationbbc('bbc 1','bbc1',"radio1","http://www.bbc.co.uk/radio/listen/live/r1_aaclca.pls",".pc-result-heading a",".pc-result-heading a")
bbc2 = stationbbc('bbc 2','bbc2',"radio2","http://www.bbc.co.uk/radio/listen/live/r2_aaclca.pls",".pc-result-heading a",".pc-result-heading a")
bbc3 = stationbbc('bbc 3','bbc3',"radio3","http://www.bbc.co.uk/radio/listen/live/r3_aaclca.pls",".pc-result-heading a",".pc-result-heading a")
bbc4 = stationbbc('bbc 4','bbc4',"radio4","http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls",".pc-result-heading a",".pc-result-heading a")
bbc5 = stationbbc('bbc 5','bbc5',"5live" ,"http://www.bbc.co.uk/radio/listen/live/r5_aaclca.pls",".pc-result-heading a",".pc-result-heading a")
bbc6 = stationbbc('bbc 6','bbc6',"6music","http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls",".pc-result-heading a",".pc-result-heading a")

BBC = stationgroup("BBC",[bbc1,bbc2,bbc3,bbc4,bbc5,bbc6])
