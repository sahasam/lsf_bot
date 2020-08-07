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
import os
import re
import requests
import sys
import urllib.request

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
        print("server response: ", auth_response)
        print(f"failed to get access token from twitch.tv: {e}")
        sys.exit(1)
    
    return access_token

def download_mp4_from_link(link, cid, access_token, output_dir) :
    slug = link.split('/')[-1]
    download_mp4_from_slug(slug, cid, access_token, output_dir)
    
def download_mp4_from_slug(slug, cid, access_token, output_dir) :
    #https://github.com/amiechen/twitch-batch-loader/blob/master/batchloader.py
    clip_info = requests.get(
        "https://api.twitch.tv/helix/clips?id=" + slug,
        headers={"Client-ID": cid, 'Authorization': f'Bearer {access_token}'}).json()

    thumb_url = clip_info['data'][0]['thumbnail_url']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'

    title = clip_info['data'][0]['title']

    regex = re.compile('[^a-zA-Z0-9_]')
    title = title.replace(' ', '_')
    out_filename = regex.sub('', title) + '.mp4'
    output_path = os.path.join(output_dir, out_filename)

    print(f"\nDownloading {title} -> {output_path}")
    urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)

#https://github.com/amiechen/twitch-batch-loader/blob/master/batchloader.py
def dl_progress (count, block_size, total_size) :
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

if __name__ == "__main__" :
    args = docopt(__doc__, version="lsfbot v1.0.0")
    config = configparser.ConfigParser()
    config.read("config.ini")

    twitch_client_id = args['--client-id'] if args['--client-id'] is not None else config['twitch oauth']['client_id']
    twitch_client_secret = args['--client-secret'] if args['--client-secret'] is not None else config['twitch oauth']['client_secret']
    output_dir = args['--output-file']

    access_token = get_twitch_authorization(twitch_client_id, twitch_client_secret)
    for link in args['<link>'] :
        try:
            download_mp4_from_link(link, twitch_client_id, access_token, output_dir)
        except KeyError:
            print("invalid link")
            continue