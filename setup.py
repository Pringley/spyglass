from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "spyglass",
    version = "0.0.1",
    packages = find_packages(),
    scripts = ['exe/spyglass'],
    
    install_requires = """
      beautifulsoup4>=4.1.2
    """,

    author = "Ben Pringle",
    author_email = "ben.pringle@gmail.com",
    description = "The Pirate Spyglass: scraper for The Pirate Bay",
    url = "http://github.com/Pringley/spyglass",
    license = "MIT",
)
