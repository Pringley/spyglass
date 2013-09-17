from __future__ import unicode_literals

from urllib2 import urlopen
from collections import namedtuple
from bs4 import BeautifulSoup

Response = namedtuple('Response', ['text', 'soup'])

def get(url):
    text = urlopen(url).read()
    soup = BeautifulSoup(text)
    return Response(text=text, soup=soup)
