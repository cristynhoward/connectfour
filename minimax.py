""" Playground for developing Minimax Connect Four opponent.
"""
from ConnectFourGame import *
import random


def minimax(game, depth):
    """ Chooses the next move in a ConnectFourGame.

    :param game: The game to choose the next move for.
    :type game: ConnectFourGame
    :param depth: The number of layers to iterate the Minimax search.
    :type depth: int
    :return: The next column to play in. 1-indexed.
    :rtype: int
    """
    best_score = -1001
    best_moves = []
    moves = {}
    i = 1

    while i < 8:
        if game.get_val(i, 0) == 0:

            copy_game = ConnectFourGame.game_from_string(game.game_to_string())
            copy_game.play_turn(0, i)

            score = 0
            if copy_game.game_won == 1:
                score = 1000

            else:
                if depth > 0:
                    opponent_move = minimax(copy_game, depth - 1)
                    copy_game.play_turn(0, opponent_move)

                    if copy_game.game_won == 1:
                        score = -1000

            moves[i] = score

            if score > best_score:
                best_score = score
                best_moves.clear()

            if score == best_score:
                best_moves.append(i)

        i += 1

    return best_moves[random.randint(0, len(best_moves) - 1)]
