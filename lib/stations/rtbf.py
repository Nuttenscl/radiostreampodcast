import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
from lib.base_podcast import emission, station, stationgroup
from prettytable import PrettyTable
import urllib2
import json
import time
import sqlite3


class stationrtbf(station):
	def __init__(self,name,nomcode="",podprefix=""):
		url="http://www.rtbf.be/"+nomcode+"/podcast?by=emission"
		#streamurl="http://statslive.rtbf.be/playlist/"+nomcode+"/"+nomcode+"-64.aac/playlist.pls"
		streamurl="http://"+nomcode+".ice.rtbf.be/"+nomcode+"-128.mp3"
		station.__init__(self,name,nomcode,url,streamurl,False,True)
		self.name=name
		self.code=nomcode
		self.url=url
		self.streamurl=streamurl
		self.argtitle="li.emissions ul li ul li a[title], li.rubriques ul li ul li a[title]"
		self.nomcode=nomcode
		self.podprefix=podprefix

	def fillemission(self,query=""):
		emissions=[]
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		page= html.parse(self.url)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
		except SelectorError:
			parser.error('Invalid CSS selector')
	
		for e in page.xpath(expressiontitle):
			try:
				found =re.search('http://www.rtbf.be/'+self.nomcode+'/.*?programId=([^"]*)', e.get("href")).group(1)
			except AttributeError:
			    found = '' 
			etemp = emissionrtbf(e.get("title"),found)
			emissions.append(etemp)
		self.emissions=emissions

	def fillemissionindb(self,query=""):
		emissions=[]
		self.cleardb()
		conn = sqlite3.connect('podcast.db')
		c = conn.cursor()
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		page= html.parse(self.url)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
		except SelectorError:
			parser.error('Invalid CSS selector')
	
		for e in page.xpath(expressiontitle):
			try:
				found =re.search('http://www.rtbf.be/'+self.nomcode+'/.*?programId=([^"]*)', e.get("href")).group(1)
			except AttributeError:
			    found = '' 
			etemp = emissionrtbf(e.get("title"),found)
			qqq = "INSERT INTO emissions (station, title, podcasturl, idemission) VALUES (\""+self.name+"\",\""+etemp.name+"\",'"+etemp.podcasturl+"','"+str(etemp.idpod)+"')"
			print qqq
			c.execute(qqq)
			emissions.append(etemp)
		self.emissions=emissions
		conn.commit()
		conn.close()


	def searchpodcast(self,query=""):
		emissions=[]
		url="http://www.rtbf.be/radio/podcast/fetchall?channel="+self.nomcode+"&tab=tags&category=all&query="+query
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		jsonurl = urllib2.urlopen(url)
		text = json.loads(jsonurl.read())
		x = PrettyTable(["id","Titre", "date","url"])
		x.align["Titre"] = "l" # Left align 
		x.align["date"] = "l" # Left align 
		x.align["url"] = "l" # Left align
		x.padding_width = 1 # One space between column edges and contents (default)
		for po,ii in zip(text['list'],range(len(text['list']))):
		    x.add_row([ ii,po['title'],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(po['created'])),po['url'] ])
		print x		

class emissionrtbf(emission):
	def __init__(self,name,idpod):
		podcasturl="http://rss.rtbf.be/media/rss/audio/c21-"+idpod+".xml"
		emission.__init__(self,name,podcasturl,idpod)
		self.idpod=idpod
		self.name=name
		self.podcasturl=podcasturl


lapremiere = stationrtbf("La premiere","lapremiere","lp")
musiq3     = stationrtbf("Musique 3","musiq3","m3")
classic21  = stationrtbf("Classic 21","classic21","c21")
purefm	   = stationrtbf("Pure fm","purefm","pu")
vivacite   = stationrtbf("Vivacite","vivacite","vi")
RTBF=stationgroup("RTBF",[lapremiere,musiq3,classic21,purefm,vivacite])
