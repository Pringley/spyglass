from urllib2 import urlopen
from collections import namedtuple
from bs4 import BeautifulSoup

Response = namedtuple('Response', ['text', 'soup'])

def get(url):
    """Query a web URL.

    Return a Response object with the following attributes:
    - text: the full text of the web page
    - soup: a BeautifulSoup object representing the web page

    """
    text = urlopen(url).read()
    soup = BeautifulSoup(text)
    return Response(text=text, soup=soup)
