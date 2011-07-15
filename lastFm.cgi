#!/usr/bin/env python

# This code was written on June 16, 2010.  I hereby
# release it into the public domain and release all rights over it.

from xml.dom import minidom
from urllib import urlopen
from time import sleep
import cgi
import sys

apiKey = 'fdb0f04d3322844d8c47c45b14a26375'
RETRIES = 5

print "Content-type: text/html; charset=utf-8\n\n"

form = cgi.FieldStorage()

username = form.getvalue("username")

print """
<html>
<body>

<p><b>last.fm PrettyPrint</b> <br /></p>
<p>Enter your last.fm username here to get a chart for your weekly top artists
with all the weird tabs and extraneous things removed, so you can easily
copy-paste it into forums and whatnot.</p>
<a href="http://www.ocf.berkeley.edu/~wsong/prettyPrintLastFmSource.py">Click
here for the source code.</a>
<form action="lastFm.cgi" method="GET">
    <p>Enter username: <input type="text" name="username"/></p>
    <p><input type="submit" value="Submit"/></p>
</form>
"""

def get_xml(u):
    for i in xrange(RETRIES):
        try:
            sleep(1)
            return minidom.parse(urlopen(u))
        except IOError:
            print "Connection to last.fm failed."

def getWeeklyTopArtists(user, api_key):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=%s&api_key=%s&period=7day' % (user, api_key)
    return get_xml(url).getElementsByTagName("artist")

def getWeeklyArtistList(xmlArtistObj):
    results = []
    for i in range(0, len(xmlArtistObj)):
        rank = xmlArtistObj[i].getAttribute("rank")
        artistName =  xmlArtistObj[i].getElementsByTagName("name")[0].firstChild.nodeValue
        playcount = xmlArtistObj[i].getElementsByTagName("playcount")[0].firstChild.nodeValue
        results.append((rank, artistName, playcount))
    return results

if(username != None):
    artists = getWeeklyArtistList(getWeeklyTopArtists(username, apiKey))
    counter = 1
    for i in range(0, len(artists)):
        if(i != 0 and artists[i - 1][2] == artists[i][2]):
            row = "%s\t%s\t%s" % (counter, artists[i][1], artists[i][2])
            unicodeRow = unicode(row)
            print unicodeRow.encode('ascii', 'xmlcharrefreplace')
            print "<br/>"
        else:
            row = "%s\t%s\t%s" % (i+1, artists[i][1], artists[i][2])
            unicodeRow = unicode(row)
            print unicodeRow.encode('ascii', 'xmlcharrefreplace')
            print "<br/>"
            counter = i + 1
else:
    print ""

print "</body>"
print "</html>"
