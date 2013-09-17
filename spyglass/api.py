from .scraper import default as default_scraper

def top(*args, **kwargs):
    return default_scraper.top(*args, **kwargs)
