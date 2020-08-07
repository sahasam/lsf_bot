"""
Livestream clip compiler bot

Usage:
    bot.py [options] 

Options:
    -h, --help                          display this
    -o, --out-file <file>               specify the output file of the final compilation
    -t, --time <time>                   specify the length of the compilation 
"""
import configparser
import os
import praw
import re
import requests
import sys
import urllib.request

from docopt import docopt

from clip_downloader import get_twitch_authorization
from clip_downloader import download_mp4_from_link

config = configparser.ConfigParser()
config.read("config.ini")

DOWNLAOD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")     
    print(args)

    access_token = get_twitch_authorization(tcid=config['twitch oauth']['client_id'],
                                           tcs=config['twitch oauth']['client_secret'])

    reddit = praw.Reddit(client_id=config['reddit oauth']['client_id'],
                        client_secret=config['reddit oauth']['client_secret'],
                        username=config['reddit oauth']['username'],
                        password=config['reddit oauth']['password'],
                        user_agent=config['reddit oauth']['user_agent'])

    subreddit = reddit.subreddit('LivestreamFail')
    hot_lsf= subreddit.hot(limit=2)

    for submission in hot_lsf :
        try:
            download_mp4_from_link(submission.url, 
                                config['twitch oauth']['client_id'], 
                                access_token, 
                                DOWNLAOD_FOLDER)
        except IndexError:
            #invalid link
            continue