import praw
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id=config['oauth']['client_id'],
                    client_secret=config['oauth']['client_secret'],
                    username=config['oauth']['username'],
                    password=config['oauth']['password'],
                    user_agent=config['oauth']['user_agent'])

subreddit = reddit.subreddit('LivestreamFails')
hot_lsf= subreddit.hot(limit=1)

for submission in hot_lsf :
    print(submission.title, submission.url)