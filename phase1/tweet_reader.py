import os, tweepy
from io.helpers import *


def get_mentions():
    api = get_twitter_api()
    SINCE_ID = get_read_since()
    mentions = []

    try:
        if (SINCE_ID == 0):
            mentions = api.mentions_timeline()
        else:
            mentions = api.mentions_timeline(SINCE_ID)

    except tweepy.error.TweepError as e:
        log(str(e.message))

    else:
        for mention in mentions:
            log("read tweet " + mention.id_str + "from " + mention.user.screen_name)
            record_reply(mention)

        if (mentions.since_id == None):
            log("No new mentions since " + str(SINCE_ID) + ".");

        else:
            new_since_id = mentions.since_id
            log("Retrieved mentions from " + str(SINCE_ID) + " to " + str(new_since_id) + ".");
            set_read_since(new_since_id)


def record_reply(tweet):
    log("enqueued reply to tweet " + tweet.id_str)
    with open(os.path.join(getpath(), '.data/queue.csv'), 'a+') as f:
        reply = tweet.id_str + "," + tweet.user.screen_name + "," + "I'm a bot that responds to mentions! :robot_face:" + "\n";
        f.write(reply)
