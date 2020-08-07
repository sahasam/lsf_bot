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

config = configparser.ConfigParser()
config.read("config.ini")

DOWNLAOD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")

def get_authorizations() :
    reddit = praw.Reddit(client_id=config['reddit oauth']['client_id'],
                        client_secret=config['reddit oauth']['client_secret'],
                        username=config['reddit oauth']['username'],
                        password=config['reddit oauth']['password'],
                        user_agent=config['reddit oauth']['user_agent'])

    auth_response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        data={"client_id": config['twitch oauth']['client_id'],
            "client_secret": config['twitch oauth']['client_secret'],
            "grant_type": "client_credentials"}).json()

    try:
        access_token = auth_response['access_token']
    except KeyError as e:
        print(auth_response)
        print(f"failed to get access token from twitch.tv: {e}")
        sys.exit(1)
    
    return reddit, access_token


def retrieve_mp4_data(slug, access_token):
    #https://github.com/amiechen/twitch-batch-loader/blob/master/batchloader.py
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": config['twitch oauth']['client_id'], 'Authorization': f'Bearer {access_token}'}).json()
    print(clip_info)

    thumb_url = clip_info['data'][0]['thumbnail_url']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'

    title = clip_info['data'][0]['title']

    return mp4_url, title

#https://github.com/amiechen/twitch-batch-loader/blob/master/batchloader.py
def dl_progress (count, block_size, total_size) :
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")     
    print(args)

    reddit, tw_access_token = get_authorizations()

    subreddit = reddit.subreddit('LivestreamFail')
    hot_lsf= subreddit.hot(limit=2)

    for submission in hot_lsf :
        slug = submission.url.split('/')[3]

        try:
            mp4_url, clip_title = retrieve_mp4_data(submission.url.split('/')[3], tw_access_token)
        except IndexError:
            #found post without a link
            continue

        regex = re.compile('[^a-zA-Z0-9_]')
        clip_title = clip_title.replace(' ', '_')
        out_filename = regex.sub('', clip_title) + '.mp4'
        output_path = os.path.join(DOWNLAOD_FOLDER, out_filename)

        print('\nDownloading clip slug: ' + slug)
        print('"' + clip_title + '" -> ' + out_filename)
        print(mp4_url)
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
        print('\nDone.')