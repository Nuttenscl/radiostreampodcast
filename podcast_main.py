#!/usr/bin/python

from lib.base_podcast import emission, station
from lib.stations.radiofrance import *
from lib.stations.rtlfrance import *
from lib.stations.rtbf import *
from lib.stations.europe1 import *
from lib.stations.bbc import *
from lib.stations.vrt import *

import readline
import os
clear = lambda: os.system('clear')

allstationgroup=[BBC,RTL,Lagardere,RadioFrance,RTBF,VRT]

allstation={}

for group in allstationgroup:
	for st in group.stations:
		allstation[st.code]=st

def complete(text, state):
    for cmd in allstation.keys():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

def clearscreen():	
	os.system('cls' if os.name == 'nt' else 'clear')

def printglobheader():
	print '---------------------------------------------'
	print '|  Radio Station stream and podcast browser |'
	print '---------------------------------------------'
def printheader(chaine):
	print '\n***************************'
	print '*  '+chaine
	print '***************************',
def printstationlist():
	for group in allstationgroup:
		print "  - "+group.name+" group :\n\t",
		for st in group.stations:
			if st.lso==True:
				lss="*"
			else :
				lss=""
			print st.name+" ("+st.code+lss+') - ', 
		print "\n"
	print " *live stream only station\n"


def main():
	menu = {}
	#menu['0']="list chaines" 
	menu['0']="podcast search"
	menu['1']="list programmes" 
	menu['2']="list and play podcast"
#	menu['3']="play podcast"
	menu['3']="play station"
	menu['4']="change station"
	menu['5']="Exit"
	while True: 
		options=menu.keys()
		options.sort()
	#	os.system('cls' if os.name == 'nt' else 'clear')
		clearscreen()
		printglobheader()
		print "\nChoose your station\n********************"
		printstationlist()
#		print ' - '.join(sorted(allstation.keys())) + " - 0 to exit"
		chaine=raw_input("station code (or exit):")
		if chaine =='0' or chaine=="exit":
			return 0
		clearscreen()
		try:
			printheader(allstation[chaine].name)
		except KeyError:
			print "wrong selection"
			continue
		if allstation[chaine] in RTBF.stations :
			options=[options[ii] for ii in (0,1,3,4,5)]
		elif allstation[chaine].lso:
			options=options[3:6]
		else:
			options=options[1:6]
		while True: 
			query=""
			print "\n"
			for entry in options: 
		  		print entry+") "+menu[entry],"  ",
			selection=raw_input("\nPlease Select action:") 
			#if selection =='0': 
			#	print ' - '.join(allstation.keys())
			if selection =='1': 
				if allstation[chaine].query :
					query=raw_input("query:") 
			  	allstation[chaine].listemissions(query)
			elif selection == '2': 
				emissid=raw_input("index programme:") 
				maxx=raw_input("how many to display?") 
				if not hasattr(allstation[chaine],"emissions"):
					if allstation[chaine].query :
						query=raw_input("query:") 
					allstation[chaine].fillemission(query)
			  	allstation[chaine].emissions[int(emissid)].listpodcasts(int(maxx))
				playapodcast=raw_input("1) Play one  2) Leave to menu\nchoice:")
				if playapodcast=='1':
					podcastid=raw_input("podcast index:") 
				  	allstation[chaine].emissions[int(emissid)].playpodcast(int(podcastid)) 
					clearscreen()
					printheader(allstation[chaine].name)
			elif selection == '0': 
				if allstation[chaine].query :
					query=raw_input("query:") 
			  	allstation[chaine].searchpodcast(query) 	
			elif selection == '3': 
				clearscreen()
				printheader(allstation[chaine].name)
				print "\n---- LIVE STREAMING -----\n     hit q to stop \n"
			  	allstation[chaine].playstation() 	
				clearscreen()
				printheader(allstation[chaine].name)
			elif selection == '4': 
			        break
			elif selection == '5': 
			  #break
		  	  return 0
			else: 
			  print "Unknown Option Selected!"
if __name__ == "__main__":
	main()
