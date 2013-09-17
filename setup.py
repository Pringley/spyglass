from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "spyglass",
    version = "0.0.1",
    packages = find_packages(),
    
    install_requires = """
      beautifulsoup4
      lxml
    """,

    author = "Ben Pringle",
    author_email = "ben.pringle@gmail.com",
    description = "The Pirate Spyglass: scraper for The Pirate Bay",
    license = "MIT",
)
