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

import queue
import threading

from docopt import docopt

from clip_downloader import get_twitch_authorization
from clip_downloader import download_mp4_from_link
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

config = configparser.ConfigParser()
config.read("config.ini")

DOWNLAOD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")

lock = threading.Lock()
download_queue = queue.Queue()

def download_worker_thread(tw_client_id, access_token, videoclips ) :
    url = download_queue.get()
    try:
        output_path = download_mp4_from_link(url, 
                            tw_client_id, 
                            access_token, 
                            DOWNLAOD_FOLDER)
    except KeyError:
        print(f"invalid link: {url}")
        return

    lock.acquire()
    videoclips.append(VideoFileClip(output_path))
    lock.release()
    download_queue.task_done()

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")     

    access_token = get_twitch_authorization(tcid=config['twitch oauth']['client_id'],
                                           tcs=config['twitch oauth']['client_secret'])

    reddit = praw.Reddit(client_id=config['reddit oauth']['client_id'],
                        client_secret=config['reddit oauth']['client_secret'],
                        username=config['reddit oauth']['username'],
                        password=config['reddit oauth']['password'],
                        user_agent=config['reddit oauth']['user_agent'])

    subreddit = reddit.subreddit('LivestreamFail')
    hot_lsf= subreddit.hot(limit=2)

    videoclips = []

    t1 = threading.Thread(target=download_worker_thread, args=(config['twitch oauth']['client_id'], access_token, videoclips))
    t2 = threading.Thread(target=download_worker_thread, args=(config['twitch oauth']['client_id'], access_token, videoclips))
    t1.start()
    t2.start()

    for submission in hot_lsf :
        download_queue.put(submission.url)
    
    t1.join()
    t2.join()

    finalclip = concatenate_videoclips(videoclips)
    finalclip.write_videofile("final compilation.mp4")