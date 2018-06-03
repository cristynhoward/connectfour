import tweepy
from time import gmtime, strftime
from secrets import *


def get_twitter_api():
    """ Use secrets to authenticate twitter API access. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)


def getpath():
    """ Returns the filepath to the present file."""
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def log(message):
    """ Log message to logfile."""
    print(message)
    day = strftime("%d_%b_%Y", gmtime())
    with open(os.path.join(getpath(), "data/logs/" + day + "_bot.log"), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def get_read_since():
    """ Get the ID of the last tweet read.

    :return: the ID of the last tweet read.
    :rtype: str
    """
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'a+') as f:
        for line in f:
            x = line.split(",")
            return x[0]


def get_last_wrote():
    """ Get the ID of the last tweet written.
    :return: the ID of the last tweet written.
    :rtype: str
    """
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'a+') as f:
        for line in f:
            x = line.split(",")
            return x[1]


def set_read_since(new):
    """ Set the ID of the last tweet read.

    :param new: the new ID of the last tweet read.
    :type new: int, str
    """
    next_write = get_last_wrote()
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'w') as f:
        f.write(str(new) + "," + next_write)


def set_last_wrote(new):
    """ Set the ID of the last tweet written.

    :param new: the next ID of the last tweet written.
    :type new: int, str
    """
    read_since = get_read_since()
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'w') as f:
        f.write(read_since + "," + str(new))
