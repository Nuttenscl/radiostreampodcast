import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
from lib.base_podcast import emission, station,stationgroup
from prettytable import PrettyTable
import sqlite3

class stationradiofrance(station):
	def __init__(self,name,code="",url="",streamurl="",titlearg="",urlarg=""):
		station.__init__(self,name,code,url,streamurl)
		self.name=name
		self.code=code
		self.url=url
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
						print(found)
					else:
						found =re.search('http.*rss_(.*)\.xml', eid.get("href")).group(1)
				except AttributeError:
				    found = '' 
			else:
				found=""
			etemp = emissionradiofrance(e.text,found)
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
						print(found)
					else:
						found =re.search('http.*rss_(.*)\.xml', eid.get("href")).group(1)
				except AttributeError:
				    found = '' 
			else:
				found=""
			etemp = emissionradiofrance(e.text,found)
			qqq = "INSERT INTO emissions (station, title, podcasturl, idemission) VALUES (\""+self.name+"\",\""+etemp.name+"\",'"+etemp.podcasturl+"','"+str(etemp.idpod)+"')"
			print(qqq)
			c.execute(qqq)
		conn.commit()
		conn.close()

class emissionradiofrance(emission):
	def __init__(self,name,idpod):
		podcasturl="http://radiofrance-podcast.net/podcast09/rss_"+str(idpod)+".xml"
		emission.__init__(self,name,podcasturl,idpod)
		self.idpod=idpod
		self.name=name
		self.podcasturl=podcasturl


inter = stationradiofrance('France Inter', "frinter","http://www.franceinter.fr/podcasts/liste","http://www.tv-radio.com/station/france_inter_mp3/france_inter_mp3-128k.m3u",".contenu h2 a",".podrss")
mouv  = stationradiofrance('Le Mouv',"lemouv","http://www.lemouv.fr/podcasts",".row .title","http://www.tv-radio.com/station/le_mouv_mp3/le_mouv_mp3-128k.m3u",".row .podcast-links a.podcast-rss")
info  = stationradiofrance('France Info',"frinfo","http://www.franceinfo.fr/programmes-chroniques/podcasts","http://www.tv-radio.com/station/france_info/france_info.m3u",".emission-gdp h2 a", ".podcast .last a")
culture = stationradiofrance('France culture',"frculture","http://www.franceculture.fr/podcasts","http://www.tv-radio.com/station/france_culture_mp3/france_culture_mp3-128k.m3u","li h3 a","li h3 a")
fip = stationradiofrance('FIP',"frfip","http://www.fipradio.fr/emissions","http://www.tv-radio.com/station/fip_mp3/fip_mp3-128k.m3u",".rubrique_emission a h1.title",".podcast_rss a")

RadioFrance = stationgroup("Radio France",[inter,mouv,info,culture,fip])
