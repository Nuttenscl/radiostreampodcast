import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
from lib.base_podcast import emission, station,stationgroup
from prettytable import PrettyTable
import sqlite3


class stationeurope1(station):
	def __init__(self,name,code,url="",streamurl="",titlearg="",urlarg=""):
		station.__init__(self,name,code,url,streamurl)
		self.name=name
		self.url=url
		self.code=code
		self.streamurl=streamurl
		self.argtitle=titlearg
		self.argurl=urlarg

	def fillemission(self,query=""):
		emissions=[]
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		page= html.parse(self.url)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
			expressionurl = GenericTranslator().css_to_xpath(self.argurl)
		except SelectorError:
			parser.error('Invalid CSS selector')
	
		for e,eid in zip(page.xpath(expressiontitle),page.xpath(expressionurl)):
			try:
				title =re.search('.* au podcast (.*)', e.text ).group(1) 
				found =re.search('^.*sound/(.*)\.xml', eid.get("href")).group(1)
			except AttributeError:
			    found = '' 
			etemp = emissioneurope1(title,found)
			emissions.append(etemp)
		self.emissions=emissions
	

	def fillemissionindb(self,query=""):
		self.cleardb()
		conn = sqlite3.connect('podcast.db')
		c = conn.cursor()
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		page= html.parse(self.url)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
			expressionurl = GenericTranslator().css_to_xpath(self.argurl)
		except SelectorError:
			parser.error('Invalid CSS selector')
	
		for e,eid in zip(page.xpath(expressiontitle),page.xpath(expressionurl)):
			try:
				title =re.search('.* au podcast (.*)', e.text ).group(1) 
				found =re.search('^.*sound/(.*)\.xml', eid.get("href")).group(1)
			except AttributeError:
			    found = '' 
			etemp = emissioneurope1(title,found)
			qqq = "INSERT INTO emissions (station, title, podcasturl, idemission) VALUES (\""+self.name+"\",\""+etemp.name+"\",'"+etemp.podcasturl+"','"+str(etemp.idpod)+"')"
			print(qqq)
			c.execute(qqq)
		conn.commit()
		conn.close()


class emissioneurope1(emission):
	def __init__(self,name,idpod):
		podcasturl="https://cdn-new-europe1.ladmedia.fr/var/exports/podcasts/sound/"+str(idpod)+".xml"
		emission.__init__(self,name,podcasturl,idpod)
		self.idpod=idpod
		self.name=name
		self.podcasturl=podcasturl


europe1 = stationeurope1("Europe 1","europe1","https://www.europe1.fr/podcasts","https://vipicecast.yacast.net/europe1",'.popup .title','.popup ul li a.link')

Lagardere = stationgroup("Lagardere",[europe1])
 
