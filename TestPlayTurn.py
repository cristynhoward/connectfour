""" Tests whether attempted turns are treated accurately.
"""
from tweet_processor import *
import unittest
import tweepy


class TestPlayTurn(unittest.TestCase):

    def setUp(self):
        self.doc = {'game': "127,fake_author,fake_player,1234,2018-07-17 00:28:59.979175,"
                            "000000000000000000000000000000000000000000,0,0,0"}
        self.fake_status = tweepy.Status()
        self.fake_status.__setattr__('id_str', '333')
        self.fake_status.__setattr__('text', "@bot_mention @opponent_mention 2")
        self.fake_status.__setattr__('in_reply_to_status_id', 1234)
        fake_player = tweepy.User()
        fake_player.__setattr__('screen_name', 'fake_player')
        self.fake_status.__setattr__('user', fake_player)

    def test_playturn(self):
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNotNone(fake_turn)
        self.assertEquals(fake_turn.user1, 'fake_author')
        self.assertEquals(fake_turn.user2, 'fake_player')
        self.assertEquals(fake_turn.last_tweet, 333)
        boardstring = fake_turn.game_to_string().split(',')[5]
        self.assertEquals(boardstring, "000000000002000000000000000000000000000000")

    def test_playturn_bad_input(self):
        self.fake_status.__setattr__('text', "@A @B 8")
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)
        self.fake_status.__setattr__('text', "@A @B -1")
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)
        self.fake_status.__setattr__('text', "@A @B goats")
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)
        self.fake_status.__setattr__('text', "blah")
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)

    def test_playturn_bad_user(self):
        self.fake_status.user.__setattr__('screen_name', 'bad_input')
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)

    def test_playturn_game_won(self):
        doc = {'game': "127,fake_author,fake_player,1234,2018-07-17 00:28:59.979175,"
                       "000000000000000000000000000000000000000000,0,0,1"}
        self.doc = doc
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)

    def test_playturn_full_col(self):
        doc = {'game': "127,fake_author,fake_player,1234,2018-07-17 00:28:59.979175,"
                       "121212121212000000000000000000000000000000,0,0,0"}
        self.doc = doc
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)

    def test_playturn_draw_game(self):
        doc = {'game': "127,fake_author,fake_player,1234,2018-07-17 00:28:59.979175,"
                       "000000000000000000000000000000000000000000,100,0,0"}
        self.doc = doc
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNone(fake_turn)

    def test_minimax_v1(self):
        self.doc = {'game': "127,fake_author, mimimax_ai_alpha,1234,2018-07-17 00:28:59.979175,"
                            "000000000002000000000000000000000000000000,1,1,0"}
        self.fake_status.user.__setattr__('screen_name', 'fake_author')
        self.fake_status.__setattr__('text', "@bot_mention 4")
        fake_turn = try_playturn(self.fake_status, self.doc)
        self.assertIsNotNone(fake_turn)
        self.assertEquals(fake_turn.num_turns, 3)
        self.assertEquals(fake_turn.last_tweet, 333)
        self.assertEquals(fake_turn.user1, 'fake_author')
        self.assertEquals(fake_turn.user2, ' mimimax_ai_alpha')
        self.assertEquals(fake_turn.user1_is_playing, 1)

if __name__ == '__main__':
    unittest.main()
