##
## query_bvg.py
##
###################################################################################
## Python script to query and display departure times of public transportation from
## bvg.de (Berlin/Brandenburg, Germany) for a given station.
##
## 
## Reference: https://github.com/honel/query_bvg
##
###################################################################################
#packages######################### requried for
import urllib                   ##  web query
from bs4 import BeautifulSoup   ##  parsing the web information
from tabulate import tabulate   ##  generate table from list
import datetime                 ##  determining system date/time
###################################################################################

## query URL
baseurl = ("https://fahrinfo.bvg.de/Fahrinfo/bin/stboard.bin/"+
#          "dn?ld=0.1&start=1&view=STATIONINFO&input=" ## german queries
           "en?ld=0.1&start=1&view=STATIONINFO&input=" ## english queries
)
#location = "Borsigwalder+Weg"
#location = "Potsdam%2C+Sternwarte"
#location = "S+Babelsberg"
location = "S%2BU+Wedding+%28Berlin%29%23900009104"

## execute web query
url = baseurl+location
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser").find("table", 
       {"class": "stationOverview"})

## remove all style/script elements
for script in soup(["style", "script"]):
    script.extract()

## extract text
text = soup.get_text()

## make "text" look nice
lines  = (line.strip() for line in text.splitlines())
pieces = [phrase.strip() for line in lines for phrase in line.split("\n")]
pieces = [item for item in pieces if not(item=='')]
outputlist = [pieces[i:i+3] for i in range(0, len(pieces),3)]

## output
print("Query: " + datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"))
print(tabulate(outputlist[1:len(outputlist)],headers=outputlist[0]))
print("(*) For this journey no estimation of departure is possible."+"\n"+
      "    The scheduled departure time is displayed.")
