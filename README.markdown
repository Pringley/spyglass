# The Pirate Spyglass

Scrape the Pirate Bay.

## Usage

### `spyglass.top()` -- most popular torrents

    for torrent in spyglass.top(10):
        print torrent.title, torrent.seeders, torrent.url
