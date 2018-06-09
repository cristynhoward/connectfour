""" Miscellaneous helper functions. """

from time import gmtime, strftime, sleep
from secrets import *
import tweepy
import os


def get_twitter_api():
    """ Use secrets to authenticate twitter API access. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)


def limit_handled(cursor):
    """ Iterates with a cursor object, pauses for 15 min when given a RateLimitException.
    Code taken from: http://docs.tweepy.org/en/v3.5.0/code_snippet.html#pagination

    :param cursor: The cursor to be rate limited.
    :type cursor: Cursor
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            sleep(15 * 60)


def getpath():
    """ Generate filepath to the present file.

    :return: filepath to the present file.
    :rtype: str
    """
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def log(message):
    """ Log a message in the bot log file.

    :param message: The message to be recorded.
    :type message: str
    :return: None
    :rtype: None
    """
    print(message)
    day = strftime("%d_%b_%Y", gmtime())
    with open(os.path.join(getpath(), "data/logs/" + day + "_bot.log"), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def get_next_game_id():
    """Get the ID for the next new game.

    :return: the ID for the next new game.
    :rtype: int
    """
    out = 0
    with open(os.path.join(getpath(), "data/next_game_id.txt"), 'r') as f:
        out = int(f.read())
    with open(os.path.join(getpath(), "data/next_game_id.txt"), 'w') as f:
        f.seek(0)
        f.write(str(out + 1))
        f.truncate()
    return out


def get_read_since():
    """ Get the ID of the last tweet read.

    :return: the ID of the last tweet read.
    :rtype: str
    """
    print("getting read since")
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'r') as f:
        print("opened file")
        for line in f:
            print(str(line))
            x = line.split(",")
            print(str(x[0]))
            return x[0]


def get_last_wrote():
    """Get the ID of the last tweet written.

    :return: the ID of the last tweet written.
    :rtype: str
    """
    with open(os.path.join(getpath(), "data/tweetinfo.csv"), 'r') as f:
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
