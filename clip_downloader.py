"""
clip_downloader.py
Streamlined commandline script to download twitch clips from twitch.tv

Usage:
    clip_downloader.py [options] [--] <link>...

Options:
    -c, --client-id <cid>                       specify client id. Defaults to value in config.ini
    -s, --client-secret <cs>                    specify client secret. Defaults to value in config.ini
    -o, --output-file <of>                      specify directory location to download clips [default: ./downloads] 
"""
import configparser
import requests
import sys
from docopt import docopt

def get_twitch_authorization(tcid, tcs) :
    auth_response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        data = {
            "client_id": tcid,
            "client_secret" : tcs,
            "grant_type" : "client_credentials"
        }
    ).json()

    try:
        access_token = auth_response['access_token']
    except KeyError as e:
        print(auth_response)
        print(f"failed to get access token from twitch.tv: {e}")
        sys.exit(1)
    
    return access_token

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")
    config = configparser.ConfigParser()
    config.read("config.ini")

    twitch_client_id = args['--client-id'] if args['--client-id'] is not None else config['twitch oauth']['client_id']
    twitch_client_secret = args['--client-secret'] if args['--client-secret'] is not None else config['twitch oauth']['client_secret']

    access_token = get_twitch_authorization(twitch_client_id, twitch_client_secret)
    for link in args['<link>'] :
        print(link)