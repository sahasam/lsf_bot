import praw
import pycurl
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id=config['reddit oauth']['client_id'],
                    client_secret=config['reddit oauth']['client_secret'],
                    username=config['reddit oauth']['username'],
                    password=config['reddit oauth']['password'],
                    user_agent=config['reddit oauth']['user_agent'])

curl = pycurl.Curl()

subreddit = reddit.subreddit('LivestreamFails')
hot_lsf= subreddit.hot(limit=1)

for submission in hot_lsf :
    print(submission.title, submission.url)