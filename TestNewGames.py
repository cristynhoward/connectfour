""" Tests whether new games are created accurately.
"""
from tweet_processor import *
import unittest
import tweepy


class TestNewGames(unittest.TestCase):

    def setUp(self):
        self.fake_status = tweepy.Status()
        self.fake_status.__setattr__('id_str', '12345678')
        self.fake_status.__setattr__('text', "some new game")
        self.fake_status.__setattr__('in_reply_to_status_id', None)

        fake_user = tweepy.User()
        fake_user.__setattr__('screen_name', 'fake_author')
        self.fake_status.__setattr__('user', fake_user)

        entities = {}
        user_mentions = []
        mentioned_user = {u'screen_name': 'mentioned_screenname'}
        user_mentions.append(mentioned_user)
        user_mentions.append(mentioned_user)
        entities[u'user_mentions'] = user_mentions
        self.fake_status.__setattr__('entities', entities)

    def test_newgame(self):
        fake_newgame = try_newgame(self.fake_status)
        self.assertIsNotNone(fake_newgame)
        self.assertEquals(fake_newgame.user1, 'fake_author')
        self.assertEquals(fake_newgame.user2, 'mentioned_screenname')
        self.assertEquals(fake_newgame.last_tweet, 12345678)

    def test_newgame_inreply(self):
        self.fake_status.__setattr__('in_reply_to_status_id', 1234)
        fake_newgame = try_newgame(self.fake_status)
        self.assertIsNone(fake_newgame)

    def test_newgame_missing_mention(self):
        self.fake_status.entities[u'user_mentions'].pop()
        fake_newgame = try_newgame(self.fake_status)
        self.assertIsNone(fake_newgame)

    def test_newgame_bad_command(self):
        self.fake_status.__setattr__('text', "some bad game")
        fake_newgame = try_newgame(self.fake_status)
        self.assertIsNone(fake_newgame)

if __name__ == '__main__':
    unittest.main()
