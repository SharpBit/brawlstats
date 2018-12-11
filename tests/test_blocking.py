import unittest
import time
import os

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('./.env'))

TOKEN = os.getenv('token')


class TestBlockingClient(unittest.TestCase):
    """Tests all methods in the blocking client that
    uses the `requests` module in `brawlstats`
    """

    def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.club_tag = 'QCGV8PG'
        self.client = brawlstats.Client(TOKEN, is_async=False, timeout=30)

    def tearDown(self):
        time.sleep(2)
        self.client.close()

    def test_get_player(self):
        player = self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    def test_get_club(self):
        club = self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    def test_get_leaderboard_player(self):
        lb = self.client.get_leaderboard('players')
        self.assertTrue(isinstance(lb, list))

    def test_get_leaderboard_club(self):
        lb = self.client.get_leaderboard('clubs')
        self.assertTrue(isinstance(lb, list))

    def test_get_events(self):
        events = self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertEqual(default.info, 'This data is updated hourly.')
        loc = self.client.get_constants('location')
        self.assertTrue(isinstance(loc, list))
        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    # Other
    def test_invalid_tag(self):
        get_profile = self.client.get_profile
        invalid_tag = 'P'
        self.assertRaises(brawlstats.NotFoundError, get_profile, invalid_tag)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.NotFoundError, get_profile, invalid_tag)
        invalid_tag = '2PPPPPPP'
        self.assertRaises(brawlstats.NotFoundError, get_profile, invalid_tag)

    def test_invalid_lb(self):
        get_lb = self.client.get_leaderboard
        invalid_type = 'test'
        invalid_count = 200
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_count)
        invalid_type = 'players'
        invalid_count = 'string'
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_count)
        invalid_type = 'players'
        invalid_count = 201
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_count)
        invalid_type = 'players'
        invalid_count = -5
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_count)


if __name__ == '__main__':
    unittest.main()