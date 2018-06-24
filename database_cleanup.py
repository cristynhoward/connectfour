""" Removes won and inactive games from database.
"""
from ConnectFourGame import ConnectFourGame
from databasehelpers import *
from datetime import *


def cleanup_active_games():
    """ Scan all documents in Active Games collection.
    Remove any that are completed or expired.

    :return: None
    :rtype: None
    """
    db = access_database()
    if db is not None:

        log("Cleaning up database.")
        for document in db.Active_Games.find():
            game_to_check = ConnectFourGame.game_from_string(document["game"])

            diff = datetime.now() - game_to_check.last_active
            if diff.days > 14:
                remove_active_game(game_to_check.last_tweet)
                log("Removed expired game: " + game_to_check.game_to_string())

            if game_to_check.game_won == 1:
                remove_active_game(game_to_check.last_tweet)
                log("Removed completed game: " + game_to_check.game_to_string())


if __name__ == '__main__':
    cleanup_active_games()
