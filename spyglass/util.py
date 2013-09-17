from urllib2 import urlopen
from collections import namedtuple

Response = namedtuple('Response', ['text'])

def get(url):
    return Response(text=urlopen(url).read())
