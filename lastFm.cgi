#!/usr/bin/env python

# This code was written on June 16, 2010.  I hereby
# release it into the public domain and release all rights over it.

from xml.dom import minidom
from urllib import urlopen
from time import sleep
import cgi
import sys

class ArtistAndPlaycount:
    def __init__(self, rank, name, playcount):
        self.rank = rank
        self.name = name
        self.playcount = playcount

apiKey = ''
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
    for i in range(RETRIES):
        try:
            return minidom.parse(urlopen(u))
        except IOError:
            print "Connection to last.fm failed."
        sleep(1)

def getWeeklyTopArtists(user, api_key):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=%s&api_key=%s&period=7day' % (user, api_key)
    return get_xml(url).getElementsByTagName("artist")

def getWeeklyArtistList(xmlArtistObj):
    results = []
    for node in xmlArtistObj:
        rank = node.getAttribute("rank")
        artistName =  node.getElementsByTagName("name")[0].firstChild.nodeValue
        playcount = node.getElementsByTagName("playcount")[0].firstChild.nodeValue
        results.append(ArtistAndPlaycount(rank, artistName, playcount))
    return results


if username:
    artists = getWeeklyArtistList(getWeeklyTopArtists(username, apiKey))
    counter = 1
    # This particular section emulates last.fm's habit of making artists that
    # have the same number of playcounts have the same numerical rank
    for i in range(len(artists)):
        if artists[i - 1].playcount != artists[i].playcount:
            counter = i + 1
        row = "%s\t%s\t%s" % (counter, artists[i].name, artists[i].playcount)
        unicodeRow = unicode(row)
        print unicodeRow.encode('ascii', 'xmlcharrefreplace')
        print "<br/>"

print "</body>"
print "</html>"
