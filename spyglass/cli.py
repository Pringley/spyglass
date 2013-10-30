from sys import argv, exit
from . import top, default_scraper

def print_usage():
    print 'Usage:'
    print '  spyglass lookup <PIRATE_BAY_URL>'
    print '  spyglass top <AMOUNT>'

def main():
    if len(argv) != 3:
        print_usage()

    elif argv[1] == 'lookup':
        url = argv[2]
        torrent = default_scraper.torrent_from_url(url)
        print torrent.as_json()

    elif argv[1] == 'top':
        amount = int(argv[2])
        for torrent in top(amount):
            print torrent.as_json()

    else:
        print_usage()
