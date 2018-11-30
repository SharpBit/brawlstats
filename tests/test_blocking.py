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
        self.band_tag = 'QCGV8PG'
        self.client = brawlstats.Client(TOKEN, is_async=False, timeout=30)

    def tearDown(self):
        time.sleep(2)
        self.client.close()

    def test_get_player(self):
        player = self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    def test_get_band(self):
        band = self.client.get_band(self.band_tag)
        self.assertEqual(band.tag, self.band_tag)

    def test_get_leaderboard_player(self):
        lb = self.client.get_leaderboard('players')
        self.assertTrue(isinstance(lb.players, list))

    def test_get_leaderboard_band(self):
        lb = self.client.get_leaderboard('bands')
        self.assertTrue(isinstance(lb.bands, list))

    def test_get_events(self):
        events = self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

    # Other
    def test_invalid_tag(self):
        get_profile = self.client.get_profile
        invalid_tag = 'P'
        self.assertRaises(brawlstats.InvalidTag, get_profile, invalid_tag)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.InvalidTag, get_profile, invalid_tag)

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