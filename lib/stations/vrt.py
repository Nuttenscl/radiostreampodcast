import feedparser
from lxml import etree,html
from cssselect import GenericTranslator, SelectorError
import re
import subprocess 
from lib.base_podcast import emission, station, stationgroup
from prettytable import PrettyTable
import sqlite3

class stationvrt(station):
	def __init__(self,name,code,url,streamurl="",):
		station.__init__(self,name,code,url,streamurl,True)
		self.name=name
		self.code=code
		self.url=url
		self.streamurl=streamurl


radio1 = stationvrt("Radio 1"         ,"radio1","https://www.radio1.be","https://mp3.streampower.be/radio1-high")
radio2 = stationvrt("Radio 2"         ,"radio2","https://www.radio2.be","https://mp3.streampower.be/radio2-high")
klara  = stationvrt("Klara"           ,"klara" ,"https://www.klara.be" ,"https://mp3.streampower.be/klara-high" )
stubru = stationvrt("Studio Brussel"  ,"stubru","https://www.stubru.be","https://mp3.streampower.be/stubru-high")
sporza = stationvrt("Sporza"          ,"sporza","https://www.sporza.be","https://mp3.streampower.be/sporza-high")
mnm    = stationvrt("MNM"             ,"mnm"   ,"https://www.mnm.be"   ,"https://mp3.streampower.be/donna-high" )

VRT = stationgroup("VRT",[radio1,radio2,klara,stubru,sporza,mnm])
