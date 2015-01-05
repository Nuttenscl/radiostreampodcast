radiostreampodcast
==================

This is a radio station command line streaming and podcast browsing software written in python. The stream and podcast playing is done using mplayer. The browsing capability make it different with usual podcast reader. You don't subscribe to podcast by providing a xml (rss) file but you browse in the command line through the station podcast (extracted from the station web page) to search for the interesting content. Depending on the station, you can choose between

	- podcast global search (RTBF group)
	- list station programmes
	- list and play podcast of a programme
    - play the station stream


run with 
`./podcast_main.py ` after giving the running permission
###currently available stations
  - BBC group :
	bbc 1 (bbc1) -  bbc 2 (bbc2) -  bbc 3 (bbc3) -  bbc 4 (bbc4) -  bbc 5 (bbc5) -  bbc 6 (bbc6)  

  - RTL group :
	RTL France (rtlfr) -  RTL2 France (rtl2fr) -  Fun Radio Fr. (funradiofr\*) -  BelRTL Belgique (belrtlbe\*) -  Radio Contact Belgique (radiocontactbe\*) -  Mint (mintbe\*) 

  - Lagardere group :
	Europe 1 (europe1)   

  - Radio France group :
	France Inter (frinter) -  Le Mouv (lemouv) -  France Info (frinfo) -  France culture (frculture) -  FIP (frfip)  

  - RTBF group :
	La premiere (lapremiere) -  Musique 3 (musiq3) -  Classic 21 (classic21) -  Pure fm (purefm) -  Vivacite (vivacite)  

  - VRT group :
	Radio 1 (radio1\*) -  Radio 2 (radio2\*) -  Klara (klara\*) -  Studio Brussel (stubru\*) -  Sporza (sporza\*) -  MNM (mnm\*)  


 \* *live stream only*

###dependencies
####python libraries:
* readline
* os
* prettytable
* feedparser
* subprocess 
* sqlite3
* lxml
* cssselect
* re

####mplayer

###example
the initial screen:
```
---------------------------------------------
|  Radio Station stream and podcast browser |
---------------------------------------------

Choose your station
********************
  - BBC group :
	bbc 1 (bbc1) -  bbc 2 (bbc2) -  bbc 3 (bbc3) -  bbc 4 (bbc4) -  bbc 5 (bbc5) -  bbc 6 (bbc6) -  

  - RTL group :
	RTL France (rtlfr) -  RTL2 France (rtl2fr) -  Fun Radio Fr. (funradiofr*) -  BelRTL Belgique (belrtlbe*) -  Radio Contact Belgique (radiocontactbe*) -  Mint (mintbe*) -  

  - Lagardere group :
	Europe 1 (europe1)   -  

  - Radio France group :
	France Inter (frinter) -  Le Mouv (lemouv) -  France Info (frinfo) -  France culture (frculture) -  FIP (frfip) -   

  - RTBF group :
	La premiere (lapremiere) -  Musique 3 (musiq3) -  Classic 21 (classic21) -  Pure fm (purefm) -  Vivacite (vivacite) -  

  - VRT group :
	Radio 1 (radio1*) -  Radio 2 (radio2*) -  Klara (klara*) -  Studio Brussel (stubru*) -  Sporza (sporza*) -  MNM (mnm*) -  

 *live stream only station

station code (or exit):
```

```
***************************
*  bbc 1
*************************** 

1) list programmes    2) list and play podcast    3) play station    4) change station    5) Exit    
Please Select action:1
+-------+----------------------------------+----------+
| index | Title                            | id       |
+-------+----------------------------------+----------+
|   0   | Annie Mac's Mini Mix             | r1mix    |
|   1   | Best of Nick Grimshaw            | r1grimmy |
|   2   | Greg James – That’s What He Said | greg     |
|   3   | Huw Stephens                     | huwintro |
|   4   | Scott Mills Daily                | mills    |
|   5   | The Matt Edmondson Show          | r1matt   |
+-------+----------------------------------+----------+

1) list programmes    2) list and play podcast    3) play station    4) change station    5) Exit    
Please Select action:2
index programme:3
how many to display?5
Emission: Huw Stephens
Auteur: BBC Radio 1
podcast xml: http://downloads.bbc.co.uk/podcasts/radio1/huwintro/rss.xml
+----+------------------------------------------------------------------+---------------------------------+---------------------------------------------------------------------------------+
| id | Titre                                                            | date                            | url                                                                             |
+----+------------------------------------------------------------------+---------------------------------+---------------------------------------------------------------------------------+
| 0  | Huw: Shamir Session, Hana and Tom Misch & Carmody 15 Dec 14      | Mon, 15 Dec 2014 19:51:00 +0000 | http://downloads.bbc.co.uk/podcasts/radio1/huwintro/huwintro_20141215-1951a.mp3 |
| 1  | Huw: Shura in session, Pretty Vicious and Strangers 08 Dec 14    | Mon, 08 Dec 2014 22:40:00 +0000 | http://downloads.bbc.co.uk/podcasts/radio1/huwintro/huwintro_20141208-2240a.mp3 |
| 2  | Huw: Raury session, Honne and Dom Robinson 01 Dec 14             | Mon, 01 Dec 2014 23:02:00 +0000 | http://downloads.bbc.co.uk/podcasts/radio1/huwintro/huwintro_20141201-2302b.mp3 |
| 3  | Huw: Låpsley session, The Bulletproof Bomb and Local F 24 Nov 14 | Mon, 24 Nov 2014 22:10:00 +0000 | http://downloads.bbc.co.uk/podcasts/radio1/huwintro/huwintro_20141124-2210a.mp3 |
| 4  | Huw: Years & Years session, MDNGHT and Seafret 17 Nov 14         | Mon, 17 Nov 2014 21:36:00 +0000 | http://downloads.bbc.co.uk/podcasts/radio1/huwintro/huwintro_20141117-2136a.mp3 |
+----+------------------------------------------------------------------+---------------------------------+---------------------------------------------------------------------------------+
1) Play one  2) Leave to menu




```
