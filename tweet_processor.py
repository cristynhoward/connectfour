""" Process mentions.
"""
from ConnectFourGame import *
from gamehelpers import *
from helpers import *


def process_mentions():
    """

    :return:
    :rtype:
    """
    api = get_twitter_api()
    first = True
    since_id = get_read_since()
    newest_tweet_id = None

    for tweet in limit_handled(tweepy.Cursor(api.mentions_timeline).items()):
        if int(tweet.id_str) <= int(since_id):
            return
        if first is True:
            newest_tweet_id = tweet.id_str
            first = False

        #  NEW GAME
        if len(tweet.entities[u'user_mentions']) > 1:  # at least one other user mentioned
            if tweet.in_reply_to_status_id is None:  # not reply to another tweet
                if len(tweet.text.split(" ")) > 1:  # has second command
                    if tweet.text.split(" ")[1] == "new":  # second command is new
                        user1 = tweet.user.screen_name
                        user2 = tweet.entities[u'user_mentions'][1][u'screen_name']
                        newgame = ConnectFourGame.new_game(get_next_game_id(), user1, user2, tweet.id_str)
                        record_game(newgame.game_to_string())
                        record_outgoing_game(newgame.game_to_string())
                        log("Created new game: " + newgame.game_to_string())
        else:
            #  PLAY TURN
            gamestring = retrieve_game(tweet.in_reply_to_status_id)
            if gamestring is not None:
                game = ConnectFourGame.game_from_string(gamestring)
                if game.game_won == 0:
                    active_user = game.user2
                    if game.a_is_playing == 1:
                        active_user = game.user1
                    if tweet.user.screen_name == active_user:
                        token = tweet.text.split(" ")[2]
                        if any(token == s for s in ["1", "2", "3", "4", "5", "6", "7"]):
                            game.play_turn(int(tweet.id_str), int(token))
                            record_game(game.game_to_string())
                            record_outgoing_game(game.game_to_string())
                            log(active_user + " played a " + token +
                                " resulting in game: " + game.game_to_string())

    log("Processed mentions from " + str(since_id) + " to " + str(newest_tweet_id) + ".")
    set_read_since(newest_tweet_id)


if __name__ == '__main__':
    process_mentions()
