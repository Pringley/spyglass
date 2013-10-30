import urlparse

from .urls import TOP
from .util import get
from .torrent import Torrent

class Scraper:
    """Scrape the Pirate Bay.

    The Scraper can either cache the information it downloads (so you don't
    have to re-scrape torrents if you access them more than once), or you can
    disable caching for fresh lookups each time.

    """
    def top(self, n=10, cache=None, prefetch=False):
        """Find the most popular torrents.

        Return an array of Torrent objects representing the top n torrents. If
        the cache option is non-None, override the Scraper's default caching
        settings.

        Use the prefetch option to hit each Torrent's info page up front
        (instead of lazy fetching the info on-demand later).

        """
        use_cache = self._use_cache(cache)
        if use_cache and len(self._top_cache) >= n:
            return self._top_cache[:n]
        soup = get(TOP).soup
        links = soup.find_all("a", class_="detLink")[:n]
        urls = [urlparse.urljoin(TOP, link.get('href')) for link in links]
        torrents = [self.torrent_from_url(url, use_cache, prefetch)
                for url in urls]
        if use_cache:
            self._top_cache = torrents
            self._add_to_torrent_cache(torrents)
        return torrents

    def __init__(self, cache=True):
        """Create a new Scraper object.

        Use the cache option to set the default caching strategy. If true, the
        scraper will remember most info it downloads from the pirate bay to
        avoid extra network connections.

        """
        self.cache = cache
        self.flush_cache()

    def flush_cache(self):
        """Reset all caches.

        Any function calls after this one will have a blank slate and need to
        query the Pirate Bay website again.

        """
        self._torrent_cache = {}
        self._top_cache = []
        self._recent_cache = []

    def torrent_from_url(self, url, cache=True, prefetch=False):
        """Create a Torrent object from a given URL.

        If the cache option is set, check to see if we already have a Torrent
        object representing it. If prefetch is set, automatically query the
        torrent's info page to fill in the torrent object. (If prefetch is
        false, then the torrent page will be queried lazily on-demand.)

        """
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
        # Check if a function should use caching.
        #
        # The argument is the function-specific cache flag. If this flag is
        # None, use the Scraper object's default cache setting. If the flag is
        # non-None, then the flag's value overrides the cache value.
        return (cache is not None and cache) or (cache is None and self.cache)

default = Scraper()
