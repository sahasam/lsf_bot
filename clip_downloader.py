"""
clip_downloader.py
Streamlined commandline script to download twitch clips from twitch.tv

Usage:
    clip_downloader.py [options] [--] <link>...

Options:
    -c, --client-id <cid>                       specify client id. Defaults to value in config.ini
    -s, --client-secret <cs>                    specify client secret. Defaults to value in config.ini
"""
import configparser
from docopt import docopt

config = configparser.ConfigParser()
config.read("config.ini")

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")

    twitch_client_id = args['--client-id'] if args['--client-id'] is not None else config['twitch oauth']['client_id']
    twitch_client_secret = args['--client-secret'] if args['--client-secret'] is not None else config['twitch oauth']['client_secret']

    for link in args['<link>'] :
        print(link)
