"""
This module contains the connect four game board and it's operations.
"""
from datetime import datetime


class ConnectFourGame:
    """ A game of connect four played by the twitter bot.
    """
    def __init__(self, game_id, user1, user2, last_tweet,
                 last_active, boardstring, a_is_playing, game_won):
        """ Create a game instance with given values.

        :param game_id: The unique game identifier.
        :type game_id: int
        :param user1: The screen name of user 1.
        :type user1: str
        :param user2: The screen name of user 2.
        :type user2: str
        :param last_tweet: The ID of the last tweet in the thread.
        :type last_tweet: int
        :param last_active: Date the game was last active.
        :type last_active: datetime
        :param boardstring: board values in top-to-bottom & left-to-right,
                            column-by-column fashion.
        :type boardstring: str
        :param a_is_playing: Indicates whose turn it is. 0 = false, 1 = true.
        :type a_is_playing: int
        :param game_won: Indicates if game is over. 0 = false, 1 = true.
        :type game_won: int
        """
        self.game_ID = game_id
        self.user1 = user1
        self.user2 = user2
        self.last_tweet = last_tweet
        self.last_active = last_active
        self.board = self.board_from_string(boardstring)
        self.a_is_playing = a_is_playing
        self.game_won = game_won

    @staticmethod
    def board_from_string(boardstring):
        """ Given a string representation of a connect four board, create a 2D int array.

        :param boardstring: a string representation of the connect four board.
        :type boardstring: str
        :return: a 2D int array representing the 7x6 connect four board.
        :rtype: int[][]
        """
        board = []
        for c in range(7):
            col = []
            for d in range(6):
                char = boardstring[c * 6 + d]
                col.append(int(char))
            board.append(col)
        return board

    @staticmethod
    def new_game(id, user1, user2, last_tweet):
        """Creates a new game.

        :param id: The unique ID of this game.
        :type id: int
        :param user1: The username of the first user.
        :type user1: str
        :param user2: The username of the first user.
        :type user2: str
        :param last_tweet: The ID of the most recent tweet in the game.
        :type last_tweet: int
        :return: A fresh connect four game.
        :rtype: ConnectFourGame
        """
        boardstring = "000000000000000000000000000000000000000000"
        game = ConnectFourGame(id, user1, user2, last_tweet, datetime.now(), boardstring, 1, 0)
        return game

    @staticmethod
    def game_from_string(gamestring):
        """ Instantiate a game with parameters encoded in a string.

        :param gamestring: Encodes the parameters of the game.
        :type gamestring: str
        :return: A game with specified parameters, or None if gamestring lacks paramaters.
        :rtype: ConnectFourGame
        """
        tokens = gamestring.split(",")
        if len(tokens) >= 8:
            datetime_object = datetime.strptime(tokens[4], '%Y-%m-%d %H:%M:%S.%f')
            game = ConnectFourGame(int(tokens[0]), tokens[1], tokens[2], int(tokens[3]),
                                   datetime_object, tokens[5], int(tokens[6]), int(tokens[7]))
            return game

    def game_to_string(self):
        """ Generate a single line string representation of the ConnectFourGame.

        :return: a string representation of the ConnectFourGame.
        :rtype: str
        """
        out = str(self.game_ID) + "," + self.user1 + "," + self.user2 + ","
        out = out + str(self.last_tweet) + "," + str(self.last_active) + ","
        for c in range(7):
            for d in range(6):
                out = out + str(self.get_val(c, d))
        out = out + "," + str(self.a_is_playing) + "," + str(self.game_won)
        return out

    def get_val(self, c, d):
        """ Get the value of a specific game board space.

        :param c: The column being accessed. Zero-indexed.
        :type c: int
        :param d: The depth being accessed. Zero-indexed.
        :type d: int
        :return: The value of the game board space.
        :rtype: int
        """
        if (-1 < c < 7) & (-1 < d < 6):
            col = self.board[c]
            return int(col[d])

    def asemoji(self):
        """ Output the game in an emojiful tweet-friendly representation.

        :return: Tweetable representation of the board game.
        :rtype: str
        """
        out = ""
        if self.game_won:
            out = out + "       GAME WON"
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
        if self.a_is_playing == 1:
            out = out + " (next)"

        out = out + "\n" + "@" + self.user2 + "   :blue_circle:"
        if self.a_is_playing != 1:
            out = out + " (next)"
        return out

    def play_turn(self, tweet_id, col):
        """ Modify the ConnectFourGame to play a turn.

        :param tweet_id: The ID of the tweet that made a play.
        :type tweet_id: int
        :param col: The column number to be played. 1-indexed.
        :type col: int
        :rtype: None
        """
        if self.game_won == 0:  # if game not over...
            self.last_active = datetime.now()
            self.last_tweet = tweet_id

            user = 2
            if self.a_is_playing == 1:
                user = 1

            self.place_piece(user, col)
            self.check_win()

            if self.a_is_playing == 1:
                self.a_is_playing = 0
            else:
                self.a_is_playing = 1

    def place_piece(self, user, column):
        """ Put a game piece in a specific column on the game board.

        :param user: The number of the user playing. 1 = red user A, 2 = blue user B.
        :type user: int
        :param column: The column number to be played in. 1-indexed.
        :type column: int
        """
        if 0 < column < 8:
            col = self.board[column - 1]

            if col[0] == 0:  # if top space in column empty,
                piece_depth = 0  # enter column

                for i in range(5):  # max five sink actions

                    if col[piece_depth + 1] < 1:  # if space below empty,
                        piece_depth += 1          # sink

                col[piece_depth] = user     # place piece

    def check_win(self):
        """ Check to see if there are any lines of 4 pieces on the board.

        :return: Whether or not the game has been won.
        :rtype: bool
        """
        win = (self.vert_win() | self.hor_win() | self.l_win() | self.r_win())
        if win:
            self.game_won = 1
        return win

    def vert_win(self):
        """ Check for vertical line of four same-coloured pieces.

        :return: Whether or not a vertical line of four same-coloured pieces exists on the board.
        :rtype: bool
        """
        for c in range(7):
            col = self.board[c]
            count = 0
            piece = 0

            for d in range(6):
                if count < 4:
                    if col[d] > 0:
                        if piece == col[d]:
                            count += 1
                        else:
                            count = 1
                    else:
                        count = 0
                piece = col[d]

            if count > 3:
                return True
        return False

    def hor_win(self):
        """ Check for horizontal line of four same-coloured pieces.

        :return: Whether or not a horizontal line of four same-coloured pieces exists on the board.
        :rtype: bool
        """
        for d in range(6):
            count = 0
            piece = 0
            for c in range(7):
                if count < 4:
                    col = self.board[c]
                    if col[d] > 0:
                        if piece == col[d]:
                            count += 1
                        else:
                            count = 1
                    else:
                        count = 0
                    piece = col[d]
            if count > 3:
                return True
        return False

    def l_win(self):
        """ Check for left-leaning diagonal line of four same-coloured pieces.

        :return: Whether or not a left-leaning diagonal line of four same-coloured
            pieces exists on the board.
        :rtype: bool
        """
        for start_row in range(3):
            for start_col in range(4):
                count = 0
                piece = 0
                for i in range(4):
                    if count < 4:
                        col = self.board[start_col + i]
                        x = col[start_row + i]
                        if x > 0:
                            if piece == x:
                                count += 1
                            else:
                                count = 1
                        else:
                            count = 0
                        piece = x
                if count > 3:
                    return True
        return False

    def r_win(self):
        """ Check for right-leaning diagonal line of four same-coloured pieces.

        :return: Whether or not a right-leaning diagonal line of four same-coloured
            pieces exists on the board.
        :rtype: bool
        """
        for sr in range(3):
            for sc in range(3, 7):
                count = 0
                piece = 0
                for i in range(4):
                    if count < 4:
                        col = self.board[sc - i]
                        x = col[sr + i]
                        if x > 0:
                            if piece == x:
                                count += 1
                            else:
                                count = 1
                        else:
                            count = 0
                        piece = x
                if count > 3:
                    return True
        return False
