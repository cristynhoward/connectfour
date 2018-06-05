from time import sleep
from helpers import *
import os


def load_next_game_reply():
    """ Return next game to be tweeted out.
    :return: next game to be tweeted out.
    :rtype: str
    """
    with open(os.path.join(getpath(), 'data/queue.csv'), 'a+') as f:
        last_wrote = get_last_wrote()
        for line in f:
            tokens = line.split(",")
            if int(tokens[3]) > int(last_wrote):
                return str(line)
        return None


def record_game(gamestring):
    """ Store gamestring as entry in gamelist.csv.

    :param gamestring: a string representation of the game to be recorded.
    :type gamestring: str
    """
    with open(os.path.join(getpath(), 'data/gamelist.csv'), 'a+') as f:
        f.write(gamestring + "\n")
    log("Recorded " + gamestring)


def retrieve_game(last_tweet_id):
    """ Retrieve from the gamelist the game whose last tweet has last_tweet_id.

    :param last_tweet_id: the ID of the last tweet in the game to be retrieved.
    :type last_tweet_id: str
    :return: gamestring of game iff game with last_tweet_id exists, else None.
    :rtype: str, None
    """
    with open(os.path.join(getpath(), 'data/gamelist.csv'), 'a+') as f:
        for line in f:
            tokens = line.split(",")
            if int(tokens[3]) == int(last_tweet_id):
                return str(line)
        return None


def record_outgoing_game(gamestring):
    """ Store gamestring as entry in queue.csv, the list for tweets waiting to be sent.

    :param gamestring: a string representation of the game to be recorded.
    :type gamestring: str
    """
    with open(os.path.join(getpath(), 'data/queue.csv'), 'a+') as f:
        f.write(gamestring + "\n")
    log("Recorded outgoing " + gamestring)


def retrieve_outgoing_game(last_tweet_id):
    """ Retrieve from the queue of games waiting to be tweeted the game whose last
    tweet has last_tweet_id.

    :param last_tweet_id: the ID of the last tweet in the game to be retrieved.
    :type last_tweet_id: str
    :return: gamestring of game iff game with last_tweet_id exists, else None.
    :rtype: str, None
    """
    with open(os.path.join(getpath(), 'data/queue.csv'), 'a+') as f:
        for line in f:
            print(line)
            tokens = line.split(",")
            if tokens[3] == last_tweet_id:
                return str(line)
        return None
