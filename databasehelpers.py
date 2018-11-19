""" Helper functions for storing ConnectFourGames in a MongoDB instance. """
import pymongo
from helpers import *
from secrets import *


def access_database():
    """ Attempt to access mLab MongoDB instance.

    :return: MongoDB Database instance, or None
    :rtype: pymongo.database.Database, None
    """
    try:
        db = pymongo.MongoClient(MY_URI).twitter_bot
        return db
    except pymongo.errors.InvalidURI:
        log("Invalid URI.")
    except pymongo.errors.ConnectionFailure:
        log("Connection failure.")


def record_in_collection(collection, game_to_insert):
    """ Insert a game into a MongoDB collection.

    :param collection: collection into which game will be inserted.
    :type collection: pymongo.collection.Collection
    :param game_to_insert: Game to be inserted into the collection.
    :type game_to_insert: ConnectFourGame
    :return: Result of attempt to insert, or False if failure.
    :rtype: pymongo.results.InsertOneResult, Boolean
    """
    gamestring = game_to_insert.game_to_string()
    out = {"_id": str(game_to_insert.last_tweet), "game": gamestring}
    try:
        result = collection.insert_one(out)

    except pymongo.errors.DuplicateKeyError as e:
        log("ERROR: Duplicate Key Error, record, " + gamestring)
        log(e)
        return False
    except pymongo.errors.ExecutionTimeout as e:
        log("ERROR: Execution Timeout, record, " + gamestring)
        log(e)
        return False
    except pymongo.errors.PyMongoError as e:
        log("ERROR: Pymongo Error, record, " + gamestring)
        log(e)
        return False

    else:
        return result


def record_outgoing_tweet(game):
    """ Add a game to the collection of outgoing tweets.

    :param game: The game to be tweeted.
    :type game: ConnectFourGame.ConnectFourGame
    :return: Result of insertion, or False if error occurred.
    :rtype: pymongo.results.InsertOneResult, Boolean
    """
    outgoing_tweets = access_database().Outgoing_Tweets
    if outgoing_tweets is None:
        return False
    else:
        result = record_in_collection(outgoing_tweets, game)
        if result is not False:
            log("Outgoing tweet recorded: " + game.game_to_string())
            return result
        else:
            log("ERROR: Outgoing tweet NOT recorded: " + game.game_to_string())
            return result


def record_active_game(game):
    """ Add a game to the collection of active games.

    :param game: The active game to be recorded.
    :type game: ConnectFourGame.ConnectFourGame
    :return: Result of insertion, or False if error occurred.
    :rtype: pymongo.results.InsertOneResult, Boolean
    """
    active_games = access_database().Active_Games
    if active_games is None:
        return False
    else:
        result = record_in_collection(active_games, game)
        if result is not False:
            log("Active game recorded: " + game.game_to_string())
            return result
        else:
            log("ERROR: Active game NOT recorded: " + game.game_to_string())
            return result


def load_next_tweet():
    """ Retrieve game with smallest last_tweet from the collection of outgoing tweets.

    :return: Outgoing game with smallest last tweet, or None if error encountered.
    :rtype: dict, None
    """
    db = access_database()
    if db is not None:
        try:
            doc = db.Outgoing_Tweets.find_one({}, projection=None, sort=[("_id", 1)])

        except pymongo.errors.PyMongoError as e:
            log("Pymongo Error, load_next_tweet:")
            log(e)

        else:
            log("Outgoing tweet retrieved: " + str(doc))
            return doc


def get_active_game(tweet_id):
    """ Retrieve game with tweet_id from the collection of active games.

    :param tweet_id: The id of the last tweet in the game to be retrieved.
    :type tweet_id: str
    :return: Active game with tweet_id, or None if Error encountered.
    :rtype: dict, None
    """
    db = access_database()
    if db is not None:
        try:
            doc = db.Active_Games.find_one({"_id": tweet_id})

        except pymongo.errors.PyMongoError as e:
            log("Pymongo Error, get_active_game, "+str(tweet_id))
            log(e)

        else:
            log("Active game retrieved: " + str(doc))
            return doc


def remove_from_collection(collection, tweet_id):
    """ Remove a game with tweet_id from a given collection.

    :param collection: the collection from which the game will be removed.
    :type collection: pymongo.collection.Collection
    :param tweet_id: The id of the last tweet of the game to be removed.
    :type tweet_id: str
    :return: Document encoding game removed, or False if error occurred.
    :rtype: dict, Boolean
    """
    try:
        result = collection.find_one_and_delete({"_id":str(tweet_id)})

    except pymongo.errors.ExecutionTimeout as e:
        log("ERROR: Execution Timeout, delete, " + tweet_id)
        log(e)
        return False
    except pymongo.errors.PyMongoError as e:
        log("ERROR: Pymongo Error, delete, " + tweet_id)
        log(e)
        return False

    else:
        return result


def remove_tweet(tweet_id):
    """ Remove game with tweet_id from the collection of outgoing tweets.

    :param tweet_id: Tweet ID of game to be removed.
    :type tweet_id: str
    :return: Document encoding game removed, or False if error encountered.
    :rtype: dict, Boolean
    """
    outgoing_tweets = access_database().Outgoing_Tweets
    if outgoing_tweets is None:
        return False
    else:
        result = remove_from_collection(outgoing_tweets, tweet_id)
        if result is not False:
            log("Outgoing tweet deleted: " + str(tweet_id))
            return result
        else:
            log("ERROR: Outgoing tweet NOT deleted: " + str(tweet_id))
            return result


def remove_active_game(tweet_id):
    """ Reemove game from the collection of active games.

    :param tweet_id: The id of the last tweet in the game to be removed.
    :type tweet_id: str
    :return: Document encoding game removed, or False if error encountered.
    :rtype: dict, Boolean
    """
    active_games = access_database().Active_Games
    if active_games is None:
        return False
    else:
        result = remove_from_collection(active_games, tweet_id)
        if result is not False:
            log("Active game deleted: " + str(tweet_id))
            return result
        else:
            log("ERROR: Active game NOT deleted: " + str(tweet_id))
            return result
