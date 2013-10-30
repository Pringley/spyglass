from .scraper import default as default_scraper

def top(*args, **kwargs):
    """See Scraper.top()."""
    return default_scraper.top(*args, **kwargs)
