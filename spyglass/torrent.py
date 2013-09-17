from __future__ import unicode_literals

import re

from .util import get

class Torrent:
    _keys = ['title', 'type', 'files', 'size', 'uploaded', 'submitter',
             'seeders', 'leechers', 'comments', 'link']

    def __init__(self, url, cache=True, prefetch=False):
        self.url = url
        self.cache = cache
        self.reset()
        if prefetch:
            if not cache:
                raise ConfigurationError("Cannot prefetch when cache disabled")
            self.fetch()

    def reset(self):
        self._attrs = {}
        self._fetched = False

    def fetch(self, cache=None):
        """Get info for this torrent from The Pirate Bay."""
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
        if item not in self._keys:
            raise KeyError(item)
        if self._use_cache(cache) and self._fetched:
            return self._attrs[item]
        info = self.fetch(cache=cache)
        return info[item]

    def __getitem__(self, item): 
        return self.get(item)

    def __getattr__(self, item): 
        if item not in self._keys:
            raise AttributeError(item)
        return self.get(item)

    def as_dict(self, cache=None, fetch=False):
        if not self._fetched and fetch:
            info = self.fetch(cache)
        elif self._use_cache(cache):
            info = self._attrs.copy()
        else:
            info = {}
        info.update({"url": self.url})
        return info

    def _use_cache(self, cache=None):
        return (cache is not None and cache) or (cache is None and self.cache)

    def keys(self):
        return self._keys

    def is_fetched(self):
        return _fetched
