# The Pirate Spyglass

Scrape the Pirate Bay.

## Installation

Install using [pip](http://pip-installer.org):

    pip install spyglass

This may require administrator/`sudo` privileges.

## Usage

There are two commands available:

### `top` -- most popular torrents

    spyglass top <N>

Look up the top N torrents. Print info about each in JSON, one torrent per
line.

### `lookup` -- look up a specific torrent

    spyglass lookup <URL>

Re-scrape a Pirate Bay URL. Print its info in JSON.
