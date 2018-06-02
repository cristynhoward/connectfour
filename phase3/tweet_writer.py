from phase2.ConnectFourGame import *
from phase3.gamehelpers import *
import emoji


def tweet():
    """
    :return:
    :rtype:
    """
    api = get_twitter_api()
    gamestring = load_next_game_reply()
    if gamestring is None:
        log("No game replies to be made.")
    else:
        try:
            game = ConnectFourGame.game_from_string(gamestring)
            sent = api.update_status(emoji.emojize(game.asemoji()), game.last_tweet)
        except tweepy.error.TweepError as e:
            log(e.message)
        else:
            set_last_wrote(game.last_tweet)
            game.last_tweet = sent.id_str
            record_game(game.game_to_string())
            log("Tweeted "+game.game_to_string())
            tweet()
            

if __name__ == '__main__':
    tweet()
