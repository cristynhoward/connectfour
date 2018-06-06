""" Module for processing mentions of the bot via the Twitter API.
"""
from ConnectFourGame import *
from databasehelpers import *
from helpers import *


def process_mentions():
    """ Scan through recent mentions and process them as appropriate.
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

        if tweet.in_reply_to_status_id is None:       # not reply to another tweet
            if len(tweet.entities[u'user_mentions']) > 1:  # > 1 other user mentioned
                if tweet.text.split(" ")[1] == "new":       # secondword is 'new'

                    #  NEW GAME
                    user1 = tweet.user.screen_name
                    user2 = tweet.entities[u'user_mentions'][1][u'screen_name']
                    newgame = ConnectFourGame.new_game(get_next_game_id(), user1, user2, tweet.id_str)
                    log("Created new game: " + newgame.game_to_string())
                    record_outgoing_tweet(newgame)

        else:
            doc = get_active_game(str(tweet.in_reply_to_status_id))
            if doc is not None:
                game = ConnectFourGame.game_from_string(doc["game"])

                active_user = game.user2
                if game.a_is_playing == 1:
                    active_user = game.user2
                token = 2
                if game.user1 == game.user2:
                    token = 1

                if (tweet.user.screen_name == active_user) & (game.game_won == 0):
                    column_played = tweet.text.split(" ")[token]
                    if any(column_played == s for s in ["1", "2", "3", "4", "5", "6", "7"]):

                        #  PLAY TURN
                        game.play_turn(int(tweet.id_str), int(column_played))
                        log(active_user + " played a " + column_played +
                            " resulting in game: " + game.game_to_string())
                        record_outgoing_tweet(game)
                        remove_active_game(tweet.in_reply_to_status_id)


if __name__ == '__main__':
    process_mentions()
