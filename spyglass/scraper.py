import requests
from bs4 import BeautifulSoup

from .urls import TOP
from .util import get

class Scraper:

    def top(self, n=10, cache=True):
        if cache and self.cache and len(self._top_cache) >= n:
            return self._top_cache[:n]
        req = get(TOP)
        soup = BeautifulSoup(req.text)
        links = soup.find_all("a", "detLink")
        self._top_cache = links
        return self._top_cache[:n]

    def __init__(self, cache=True):
        self.cache = cache
        self.flush_cache()

    def flush_cache(self):
        self._torrent_cache = {}
        self._top_cache = []
        self._recent_cache = []

default = Scraper()
