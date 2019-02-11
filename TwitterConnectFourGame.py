"""
This class extends the ConnectFourGame to work with the Twitter API.
"""
from ConnectFourGame import ConnectFourGame
from datetime import datetime


class TwitterConnectFourGame(ConnectFourGame):
    """ A game of connect four played by the twitter bot.
    """

    def __init__(self, game_id, boardstring, num_turns, user1_is_playing, game_won,
                 user1, user2, last_tweet, last_active):
        """ Create a game instance with given values.

        :param game_id: int. The unique game identifier.
        :param boardstring: str. Board values in top-to-bottom & left-to-right,
                            column-by-column fashion.
        :param num_turns: int. Number of moves played on game so far.
        :param user1_is_playing: int. Indicates whose turn it is. 0 = false, 1 = true.
        :param game_won: int. Indicates if game is over. 0 = false, 1 = true.
        :param user1: str. The screen name of user 1.
        :param user2: str. The screen name of user 2.
        :param last_tweet: int. The ID of the last tweet in the thread.
        :param last_active: datetime. Date the game was last active.
        """
        super(TwitterConnectFourGame, self).__init__(game_id, boardstring, num_turns,
                                                     user1_is_playing, game_won)
        self.user1 = user1
        self.user2 = user2
        self.last_tweet = last_tweet
        self.last_active = last_active

    @staticmethod
    def tcfg_from_super(cfg, user1, user2, last_tweet):
        return TwitterConnectFourGame(cfg.game_ID, cfg.board_from_string,
                                      cfg.num_turns, cfg.user1_is_playing, cfg.game_won,
                                      user1, user2, last_tweet, datetime.now())

    @staticmethod
    def new_tcfg(game_id, user1, user2, last_tweet):
        """Creates a new game.

        :param game_id: int. The unique ID of this game.
        :param user1: str. The username of the first user.
        :param user2: str. The username of the first user.
        :param last_tweet: int. The ID of the most recent tweet in the game.
        :return: TwitterConnectFourGame; A fresh connect four game.
        """
        new_game = ConnectFourGame.new_game(game_id)
        return TwitterConnectFourGame.tcfg_from_super(new_game, user1, user2, last_tweet)

    @staticmethod
    def game_from_string(gamestring):
        """ Instantiate a game with parameters encoded in a string.

        :param gamestring: Encodes the parameters of the game.
        :type gamestring: str
        :return: A game with specified parameters, or None if gamestring lacks paramaters.
        :rtype: TwitterConnectFourGame, None
        """
        tokens = gamestring.split(",")
        base = ConnectFourGame.game_from_string(gamestring)
        return TwitterConnectFourGame.tcfg_from_super(base, tokens[5], tokens[6], int(tokens[7]))

    def game_to_string(self):
        """ Generate a single line string representation of the ConnectFourGame.

        :return: a string representation of the ConnectFourGame.
        :rtype: str
        """
        out = ConnectFourGame.game_to_string(self)
        out = out + "," + self.user1
        out = out + "," + self.user2
        out = out + "," + str(self.last_tweet)
        out = out + "," + str(self.last_active)
        return out

    def get_unique_id(self):
        """ Generate a unique identifier for this TwitterConnectFourGame at 
        it's current state of play.
        """
        return str(self.last_tweet)

    def play_turn_tcfg(self, tweet_id, col):
        """ Modify the ConnectFourGame to play a turn.

        :param tweet_id: int; The ID of the tweet that made a play.
        :param col: int; The column number to be played. 1-indexed.
        :rtype: None
        """
        if self.can_play(col):
            ConnectFourGame.play_turn(self, col)
            self.last_active = datetime.now()
            self.last_tweet = tweet_id

    def asemoji(self):
        """ Output the game in an emojiful tweet-friendly representation.

        :return: Tweetable representation of the board game.
        :rtype: str
        """
        out = "@"
        if self.user1_is_playing == 1:
            out = out + self.user2
        else:
            out = out + self.user1

        out = out + "\n"
        if self.game_won:
            out = out + "       GAME WON\n"
        out = out + "\n"

        for d in range(6):
            for c in range(7):
                x = self.get_val(c, d)
                if x == 1:
                    out = out + ":red_circle:"
                if x == 2:
                    out = out + ":blue_circle:"
                if (x != 1) & (x != 2):
                    out = out + ":white_circle:"
            out = out + "\n"

        out = out + "\n@" + self.user1 + "   :red_circle:"
        if self.user1_is_playing == 1:
            out = out + " :UP!_button:"

        out = out + "\n" + "@" + self.user2 + "   :blue_circle:"
        if self.user1_is_playing != 1:
            out = out + " :UP!_button:"

        return out

