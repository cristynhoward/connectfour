""" Module for sending out tweets via the Twitter API. """
import emoji
from ConnectFourGame import *
from databasehelpers import *
from helpers import *


def tweet():
    """ Send out as many outgoing tweets as the RateLimit allows.
    """
    api = get_twitter_api()
    doc = load_next_tweet()
    if doc is None:
        log("No game replies to be made.")
    else:
        game = ConnectFourGame.game_from_string(doc["game"])
        try:
            sent = api.update_status(emoji.emojize(game.asemoji()), game.last_tweet)
        except tweepy.error.TweepError as e:
            log("TweepyError: "+ e.response.text)
            if e.response.text["errors"]["code"] in [187, "187"]: # if Status is a duplicate.
                remove_tweet(game.last_tweet)
        else:
            remove_tweet(game.last_tweet)
            set_last_wrote(sent.id_str)
            game.last_tweet = sent.id_str
            log("Tweeted " + game.game_to_string())
            record_active_game(game)
            tweet()


if __name__ == '__main__':
    tweet()
