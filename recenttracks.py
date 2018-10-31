import datetime
import urllib.parse
import urllib.request
import xml.dom.minidom

user = ''
api_key = '' 

def get_recent_tracks(user, api_key):
    from_time = datetime.datetime.strptime("2017-09-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    to_time = datetime.datetime.strptime("2017-10-06T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    args = {
        "method": "user.getRecentTracks",
        "from": int(from_time.timestamp()),
        "to": int(to_time.timestamp()),
        "limit": "200",
        "api_key": api_key,
        "user": user
    }
    url_parts = list(urllib.parse.urlparse("http://ws.audioscrobbler.com/2.0/"))
    url_parts[4] = urllib.parse.urlencode(args)
    u = urllib.parse.urlunparse(url_parts)
    xml_doc = xml.dom.minidom.parse(urllib.request.urlopen(u))
    return xml_doc.getElementsByTagName("track")

def parse_recent_tracks(xml_obj):
    results = []
    for x in xml_obj:
        date = x.getElementsByTagName("date")[0].firstChild.nodeValue
        artistName = x.getElementsByTagName("artist")[0].firstChild.nodeValue
        name = x.getElementsByTagName("name")[0].firstChild.nodeValue
        results.append((date, artistName, name))
    return results

if __name__ == "__main__":
    tracks = parse_recent_tracks(get_recent_tracks(user, api_key))
    for track in reversed(tracks):
        print(track)
