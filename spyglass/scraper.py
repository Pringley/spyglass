import urlparse

from .urls import TOP
from .util import get
from .torrent import Torrent

class Scraper:

    def top(self, n=10, cache=None, prefetch=False):
        if self._use_cache(cache) and len(self._top_cache) >= n:
            return self._top_cache[:n]
        soup = get(TOP).soup
        links = soup.find_all("a", class_="detLink")
        urls = [urlparse.urljoin(TOP, link.get('href')) for link in links]
        torrents = [self.torrent_from_url(url, cache, prefetch)
                for url in urls]
        if self._use_cache(cache):
            self._top_cache = torrents
            self._add_to_torrent_cache(torrents)
        return torrents[:n]

    def __init__(self, cache=True):
        self.cache = cache
        self.flush_cache()

    def flush_cache(self):
        self._torrent_cache = {}
        self._top_cache = []
        self._recent_cache = []

    def torrent_from_url(self, url, cache=True, prefetch=False):
        if self._use_cache(cache) and url in self._torrent_cache:
            return self._torrent_cache[url]
        torrent = Torrent(url, cache, prefetch)
        if cache:
            self._torrent_cache[url] = torrent
        return torrent

    def _add_to_torrent_cache(self, torrents):
        self._torrent_cache.update(dict((torrent.url, torrent)
            for torrent in torrents))

    def _use_cache(self, cache=None):
        return (cache is not None and cache) or (cache is None and self.cache)


default = Scraper()
