import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
from lib.base_podcast import emission, station, stationgroup
from prettytable import PrettyTable


class stationrtl(station):
	def __init__(self,name,code,url="",streamurl="",titlearg="",podcastarg="a",qu=False):
		station.__init__(self,name,code,url,streamurl,False,qu)
		self.name=name
		self.code=code
		self.url=url
		self.streamurl=streamurl
		self.argpodcast=podcastarg
		self.argtitle=titlearg

	def fillemission(self,query):
		emissions=[]
		html_parser = etree.HTMLParser(encoding='utf-8', recover=True,strip_cdata=True)
		theurl=self.url+query
		page= html.parse(theurl)
	
		try:
			expressiontitle = GenericTranslator().css_to_xpath(self.argtitle)
			expressionurl   = GenericTranslator().css_to_xpath(self.argpodcast)
		except SelectorError:
			parser.error('Invalid CSS selector')
		if self.code=="rtlfr":
			for e in page.xpath(expressiontitle):
				try:
					found =re.search('http://www.rtl.fr/emission/([^"]*)', e.get("href")).group(1)
				except AttributeError:
				    found = '' 
				etemp = emissionrtl(e.get("title"),found)
				emissions.append(etemp)

		elif self.code=="rtl2fr":
			for e,eid in zip(page.xpath(expressiontitle),page.xpath(expressionurl)):
				if eid.get("href"):
					try:
						found =re.search('http://www.rtl2.fr/podcast/(.*).xml', eid.get("href")).group(1)
					except AttributeError:
					    found = '' 
				else:
					    found=""
			#	print eid.get("href")+"  "+found+"  "+e.text
				etemp = emissionrtl(e.text,found,True)
				emissions.append(etemp)
		self.emissions=emissions



class emissionrtl(emission):
	def __init__(self,name,idpod,rtl2=False):
		podcasturl="http://www.rtl.fr/podcast/"+idpod+".xml"
		if rtl2:
			podcasturl="http://www.rtl2.fr/podcast/"+idpod+".xml"
		emission.__init__(self,name,podcasturl,idpod)



rtlfr  = stationrtl("RTL France","rtlfr","http://www.rtl.fr/recherche?type=emission&query=","http://radio.rtl.fr/rtl.pls",'.show figure a.post-link',True)
rtl2fr = stationrtl("RTL France","rtl2fr","http://www.rtl2.fr/radio/podcasts.html#","http://streaming.radio.rtl2.fr/rtl2-1-44-128",'.common h3',".common .rss")
funradiofr = station("Fun Radio Fr.","funradiofr","http://www.funradio.fr/","http://streaming.radio.funradio.fr:80/fun-1-44-128",True)

belrtlbe = station("BelRTL Belgique","belrtlbe","http://www.rtl.be/belrtl/","http://icy.rtl.nl/belrtl128",True)
radiocontactbe = station("Radio Contact Belgique","radiocontactbe","http://fr.radiocontact.be/","http://icy.rtl.nl/contactfr.m3u",True)
mintbe = station("Mint","mintbe","http://www.mint.be/","http://icy.rtl.nl/mint.m3u",True)

RTL = stationgroup("RTL",[rtlfr,rtl2fr,funradiofr,belrtlbe,radiocontactbe,mintbe])
