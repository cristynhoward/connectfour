""" Helper functions for storing games in a MongoDB instance. """
import pymongo
from helpers import *
from secrets import *


def record_outgoing_tweet(game):
    """ Add a game to the collection of outgoing tweets.

    :param game: The game to be tweeted.
    :type game: ConnectFourGame.ConnectFourGame
    """
    db = pymongo.MongoClient(MY_URI).twitter_bot
    out = { "_id" : str(game.last_tweet), "game": game.game_to_string()}
    db.Outgoing_Tweets.insert_one(out)
    log("Outgoing tweet recorded: "+game.game_to_string())


def load_next_tweet():
    """ Retrieve and remove game with smallest last_tweet from the collection of outgoing tweets.

    :return: Outgoing game with smallest last tweet.
    :rtype: dict
    """
    db = pymongo.MongoClient(MY_URI).twitter_bot
    doc = db.Outgoing_Tweets.find_one_and_delete({}, projection=None, sort=[("_id", 1)])
    log("Outgoing tweet retrieved and deleted: " + str(doc))
    return doc


def record_active_game(game):
    """ Add a game to the collection of active games.

    :param game: The game to be tweeted.
    :type game: ConnectFourGame.ConnectFourGame
    """
    db = pymongo.MongoClient(MY_URI).twitter_bot
    out = {"_id": str(game.last_tweet), "game": game.game_to_string()}
    db.Active_Games.insert_one(out)
    log("Active game recorded: " + game.game_to_string())


def get_active_game(tweet_id):
    """ Retrieve and remove game from the collection of active games.

    :param tweet_id: The id of the last tweet in the game to be retrieved.
    :type tweet_id: str
    :return: Active game with tweet_id.
    :rtype: dict
    """
    db = pymongo.MongoClient(MY_URI).twitter_bot
    doc = db.Active_Games.find_one_and_delete({"_id": tweet_id})
    log("Active game retrieved and deleted: " + str(doc))
    return doc
