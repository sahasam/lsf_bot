import praw
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

reddit = praw.Reddit(client_id='Jss7fU-QoPxedA',
                    client_secret='4bRHyJaGXrwLfM5Uy1t9XIva1go',
                    username='baption0',
                    password='munamala09',
                    user_agent='lsf_bot')

subreddit = reddit.subreddit('LivestreamFails')
hot_lsf= subreddit.hot(limit=1)

for submission in hot_lsf :
    print(submission.title, submission.url)