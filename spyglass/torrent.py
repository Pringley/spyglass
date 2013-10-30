import re

from .util import get

class Torrent:
    """Represent a torrent from TPB.

    The torrent exists in three modes:

    -   Cache=False: a network connection will be created each time any
        property is accessed (to get the most current data).

    -   Cache=True and prefetch=True: all torrent info will be downloaded on
        creation and saved for each property access.

    -   Cache=True and prefetch=False: torrent info will be lazy-fetched when
        needed, but then saved for subsequent property accesses.

    """
    _keys = ['title', 'type', 'files', 'size', 'uploaded', 'submitter',
             'seeders', 'leechers', 'comments', 'link']

    def __init__(self, url, cache=True, prefetch=False):
        """Create a Torrent object representing a URL.

        The URL should be the info page on The Pirate Bay, not the magnet link.

        Set the cache flag to False if you want the page re-queried on each
        property access. Set the prefetch flag to True to disable lazy
        fetching.

        """
        self.url = url
        self.cache = cache
        self.reset()
        if prefetch:
            if not cache:
                raise ConfigurationError("Cannot prefetch when cache disabled")
            self.fetch()

    def reset(self):
        """Reset the cache."""
        self._attrs = {}
        self._fetched = False

    def fetch(self, cache=None):
        """Query the info page to fill in the property cache.

        Return a dictionary with the fetched properties and values.

        """
        self.reset()
        soup = get(self.url).soup
        details = soup.find(id="detailsframe")
        getdef = lambda s: [elem
                for elem in details.find("dt",
                text=re.compile(s)).next_siblings
                if elem.name == 'dd'][0]
        getdefstring = lambda s: getdef(s).string.strip()
        info = {
            "title": details.find(id="title").string.strip(),
            "type": getdefstring("Type:"),
            "files": getdefstring("Files:"),
            "size": getdefstring("Size:"),
            "uploaded": getdefstring("Uploaded:"),
            "submitter": getdef("By:").parent.find("a", href=re.compile("user")).string.strip(),
            "seeders": getdefstring("Seeders:"),
            "leechers": getdefstring("Leechers:"),
            "comments": details.find(id="NumComments").string.strip(),
            "link": details.find("a", href=re.compile("^magnet\:"))['href'].strip(),
        }
        if self._use_cache(cache):
            self._attrs = info
        self._fetched = True
        return info

    def get(self, item, cache=None):
        """Lookup a torrent info property.

        If cache is True, check the cache first. If the cache is empty, then
        fetch torrent info before returning it.

        """
        if item not in self._keys:
            raise KeyError(item)
        if self._use_cache(cache) and (self._fetched or
                item in self._attrs):
            return self._attrs[item]
        info = self.fetch(cache=cache)
        return info[item]

    def set(self, item, value):
        """Add an value to the cache."""
        self._attrs[item] = value

    def __getitem__(self, item): 
        return self.get(item)

    def __getattr__(self, item): 
        if item not in self._keys:
            raise AttributeError(item)
        return self.get(item)

    def as_dict(self, cache=None, fetch=False):
        """Return torrent properties as a dictionary.

        Set the cache flag to False to disable the cache. On the other hand,
        set the fetch flag to False to avoid fetching data if it's not cached.

        """
        if not self._fetched and fetch:
            info = self.fetch(cache)
        elif self._use_cache(cache):
            info = self._attrs.copy()
        else:
            info = {}
        info.update(url=self.url)
        return info

    def _use_cache(self, cache=None):
        return (cache is not None and cache) or (cache is None and self.cache)

    def keys(self):
        return self._keys

    def is_fetched(self):
        """Return True if all properties have been fetched."""
        return _fetched
