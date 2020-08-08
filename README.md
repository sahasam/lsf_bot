# Twitch Clip Compiler Bot
This is just an attempt to prove a point that some youtubers can be outdone by content bots.

However, this repository also contains a useful script to download *any number* of twitch clips from the command line
easily

## Clip Downloader
Usage:

`python clip_downloader.py -c [client-id] -s [client-secret] -- [link1] [link2]...`


if the client-id, or the client-secret are not specified, then it will pull the information from the config file.
This may be useful if you don't want to dig up your client-id/client-secret every time you want to download something

to specify the download location:

`python clip_downloader.py -o "<folder name>" -- [link1] [link2]...`

if the download location is not specified, the clips will download to `./downloads/` from your current directory
if the folder does not exist, the program will throw an error and stop (will fix soon)

### Setup
In order to use `clip_downloader.py`, you need to get the oauth tokens from twitch.tv

#### Step 1:
go to https://dev.twitch.tv/console/ and register your app to get a client-id, and client-secret

#### Step 2:
copy and paste your client-id, and client-secret into the values in `config.ini`
