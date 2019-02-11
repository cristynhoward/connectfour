"""
This module contains the connect four game board and it's operations.
"""


class ConnectFourGame:
    """ A game of connect four.
    """

    def __init__(self, game_id, boardstring, num_turns, user1_is_playing, game_won):
        """ Create a game instance with given values.

        :param game_id: int; The unique game identifier.
        :param boardstring: str; board values in top-to-bottom & left-to-right,
                            column-by-column fashion.
        :param num_turns: int; Number of moves played on game so far.
        :param user1_is_playing: int; Indicates whose turn it is. 0 = false, 1 = true.
        :param game_won: int; Indicates if game is over. 0 = false, 1 = true.
        """
        self.game_ID = game_id
        self.board = self.board_from_string(boardstring)
        self.num_turns = num_turns
        self.user1_is_playing = user1_is_playing
        self.game_won = game_won

    @staticmethod
    def new_game(game_id):
        """Creates a new game.

        :param game_id: int; The unique ID of this game.
        :return: A fresh connect four game.
        :rtype: ConnectFourGame
        """
        boardstring = "000000000000000000000000000000000000000000"
        return ConnectFourGame(game_id, boardstring, 0, 0, 0)

    @staticmethod
    def board_from_string(boardstring):
        """ Given a string representation of a connect four board, create a 2D int array.

        :param boardstring: str; a string representation of the connect four board.
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

    def board_to_string(self):
        out = ""
        for c in range(7):
            for d in range(6):
                out = out + str(self.get_val(c, d))
        return out

    @staticmethod
    def game_from_string(gamestring):
        """ Instantiate a game with parameters encoded in a string.

        :param gamestring: str; Encodes the parameters of the game.
        :return: A game with specified parameters, or None if gamestring lacks paramaters.
        :rtype: ConnectFourGame
        """
        tokens = gamestring.split(",")
        return ConnectFourGame(int(tokens[0]), tokens[1], int(tokens[2]),
                               int(tokens[3]), int(tokens[4]))

    def game_to_string(self):
        """ Generate a single line string representation of the ConnectFourGame.

        :return: str; a string representation of the ConnectFourGame.
        """
        out = str(self.game_ID)
        out = out + "," + self.board_to_string()
        out = out + "," + str(self.num_turns)
        out = out + "," + str(self.user1_is_playing)
        return out + "," + str(self.game_won)

    def get_unique_id(self):
        """ Generate unique identifier for ConnectFourGame at current state of play.
        """
        return str(self.game_ID) + '_' + str(self.num_turns)

    def get_val(self, c, d):
        """ Get the value of a specific game board space.

        :param c: int; The column being accessed. Zero-indexed.
        :param d: int; The depth being accessed. Zero-indexed.
        :return: int; The value of the game board space.
        """
        if (-1 < c < 7) & (-1 < d < 6):
            col = self.board[c]
            return int(col[d])

    def can_play(self, col):
        """ Check that game and column can be played on.

        :param col: int; The column being accessed. 1-indexed.
        :return: bool; Whether user can play on this game in column.
        """
        return self.game_won == 0 and self.num_turns < 42 and self.get_val(col - 1, 0) == 0

    def play_turn(self, col):
        """ Modify the ConnectFourGame to play a turn.

        :param col: int; The column number to be played. 1-indexed.
        :rtype: None
        """
        if self.can_play(col):

            user = 2
            if self.user1_is_playing == 1:
                user = 1

            self.place_piece(user, col)
            self.check_win()

            self.user1_is_playing = abs(self.user1_is_playing - 1)
            self.num_turns += 1

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
                        piece_depth += 1  # sink

                col[piece_depth] = user  # place piece

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
