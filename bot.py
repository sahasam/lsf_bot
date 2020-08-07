import configparser
import os
import praw
import re
import requests
import sys
import urllib.request

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id=config['reddit oauth']['client_id'],
                    client_secret=config['reddit oauth']['client_secret'],
                    username=config['reddit oauth']['username'],
                    password=config['reddit oauth']['password'],
                    user_agent=config['reddit oauth']['user_agent'])

auth_response = requests.post(
    'https://id.twitch.tv/oauth2/token',
    data={"client_id": 'b9rd7sja03tjfxs7vv1gwk2ep4hh2w',
            "client_secret": 'e9gqrs4uvgosodwg2qxjviy8jqxa83',
            "grant_type": "client_credentials"}).json()

try:
    access_token = auth_response['access_token']
except KeyError as e:
    print(auth_response)
    print("failed to get access token from twitch.tv: {e}")
    sys.exit(1)

DOWNLAOD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")

def retrieve_mp4_data(slug):
    #https://github.com/amiechen/twitch-batch-loader/blob/master/batchloader.py
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": 'b9rd7sja03tjfxs7vv1gwk2ep4hh2w', 'Authorization': f'Bearer {access_token}'}).json()

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

subreddit = reddit.subreddit('LivestreamFails')
hot_lsf= subreddit.hot(limit=1)

for submission in hot_lsf :
    print(submission.title, submission.url.split('/')[3])

    slug = submission.url.split('/')[3]
    mp4_url, clip_title = retrieve_mp4_data(submission.url.split('/')[3])
    regex = re.compile('[^a-zA-Z0-9_]')
    clip_title = clip_title.replace(' ', '_')
    out_filename = regex.sub('', clip_title) + '.mp4'
    output_path = os.path.join(DOWNLAOD_FOLDER, out_filename)

    print('\nDownloading clip slug: ' + slug)
    print('"' + clip_title + '" -> ' + out_filename)
    print(mp4_url)
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
    print('\nDone.')