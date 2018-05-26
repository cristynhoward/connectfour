import os, tweepy, emoji
from io.helpers import *


def load_next_reply():
    with open(os.path.join(getpath(), '.data/queue.csv'), 'a+') as f:
        for line in f:
            tokens = line.split(",")
            if (tokens[0] > get_last_wrote()):
                print("ok")
                return tokens
        return None


def tweet():
    """Send out the next tweet."""
    api = get_twitter_api()
    reply = load_next_reply()
    if (reply == None):
        log("No replies to be made.")
    else:
        try:
            sent = api.update_status(emoji.emojize("Hi @" + reply[1] + ": " + reply[2]), reply[0])
        except tweepy.error.TweepError as e:
            log(e.message)
        else:
            set_last_wrote(sent.id_str)
            log("To user " + reply[1] + ", tweeted: " + reply[2])
            tweet()
