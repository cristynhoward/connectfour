""" Module for processing mentions of the bot via the Twitter API.
"""
from ConnectFourGame import *
from databasehelpers import *
from helpers import *


def process_mentions():
    """ Scan through recent mentions and send them to be processed.
    """
    api = get_twitter_api()
    first = True
    since_id = get_read_since()
    newest_tweet_id = None

    for tweet in limit_handled(tweepy.Cursor(api.mentions_timeline).items()):

        if int(tweet.id_str) <= int(since_id):  # if tweet has already been processed...
            if first is True:  # & we haven't seen any other tweets yet:
                log("No new mentions to process.")
            else:  # we have processed other tweets, thus:
                log("Processed mentions from " + str(since_id) + " to " + str(newest_tweet_id) + ".")
                set_read_since(newest_tweet_id)
            return

        if first is True:  # Collect ID of first tweet processed.
            newest_tweet_id = tweet.id_str
            first = False

        if tweet.in_reply_to_status_id is None:  # Check if mention opens a valid game.
            result_newgame = try_newgame(tweet)
            if result_newgame is not None:
                record_outgoing_tweet(result_newgame)

        else:   # Check if mention is a valid play on an existing game.
            doc = get_active_game(str(tweet.in_reply_to_status_id))
            if doc is not None:
                result_game = try_playturn(tweet, doc)
                if result_game is not None:
                    record_outgoing_tweet(result_game)
                    remove_active_game(str(tweet.in_reply_to_status_id))


def try_newgame(tweet):
    """ Process a single attempted new game.

    :param tweet: The tweet to be processed as new game.
    :type tweet: Tweepy.Status, dict
    :return: The resulting new game, or None if no new game made.
    :rtype: None, ConnectFourGame
    """
    if tweet.in_reply_to_status_id is None:             # not reply to another tweet
        if len(tweet.entities[u'user_mentions']) > 1:   # > 1 other user mentioned
            if tweet.text.split(" ")[1] == "new":       # second word is 'new'
                user1 = tweet.user.screen_name
                user2 = tweet.entities[u'user_mentions'][1][u'screen_name']
                newgame = ConnectFourGame.new_game(get_next_game_id(), user1, user2, int(tweet.id_str))
                log("Created new game: " + newgame.game_to_string())
                return newgame


def try_playturn(tweet, doc):
    """ Process a single tweet as an attempted move on an open game.

    :param tweet: The tweet to be processed as an attempted move on an open game.
    :type tweet: Tweepy.Status, dict
    :param doc: The database item storing the game onto which the turn is played.
    :type doc: dict
    :return: The resulting game after the move is played, or None if move not played.
    :rtype: ConnectFourGame, None
    """

    game = ConnectFourGame.game_from_string(doc["game"])

    active_user = game.user2
    if game.user1_is_playing == 1:
        active_user = game.user1

    move_index = 2
    if game.user1 == game.user2:
        move_index = 1

    tweet_text = tweet.text.split(" ")
    if len(tweet_text) >= move_index + 1:

        column_played = tweet_text[move_index]
        if any(column_played == s for s in ["1", "2", "3", "4", "5", "6", "7"]):
            if (tweet.user.screen_name == active_user) & game.can_play(int(column_played)):
                #  PLAY TURN
                game.play_turn(int(tweet.id_str), int(column_played))
                log(active_user + " played a " + column_played + " resulting in game: " + game.game_to_string())
                return game


if __name__ == '__main__':
    process_mentions()
