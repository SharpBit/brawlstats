import datetime
import logging
import unittest
import os
import time

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
        self.client = brawlstats.Client(
            TOKEN,
            is_async=False,
            timeout=30,
            debug=True
        )
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        time.sleep(1)
        self.client.close()

    def test_get_player(self):
        player = self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    def test_get_club(self):
        club = self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    def test_get_leaderboard_player(self):
        lb = self.client.get_leaderboard('players')
        self.assertTrue(isinstance(lb, brawlstats.Leaderboard))
        region = self.client.get_leaderboard('players', region='us')
        self.assertTrue(isinstance(region, brawlstats.Leaderboard))

    def test_get_leaderboard_club(self):
        lb = self.client.get_leaderboard('clubs')
        self.assertTrue(isinstance(lb, brawlstats.Leaderboard))

    def test_get_leaderboard_brawler(self):
        lb = self.client.get_leaderboard('shelly')
        self.assertTrue(isinstance(lb, brawlstats.Leaderboard))

    def test_get_events(self):
        events = self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertTrue(isinstance(default, brawlstats.Constants))
        maps = self.client.get_constants('maps')
        self.assertTrue(isinstance(maps, brawlstats.Constants))
        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    def test_get_misc(self):
        misc = self.client.get_misc()
        self.assertEqual(misc.server_date_year, datetime.date.today().year)

    def test_club_search(self):
        search = self.client.search_club('Penguin Raft')
        self.assertTrue(isinstance(search, list))

    def test_battle_logs(self):
        logs = self.client.get_battle_logs(self.player_tag)
        self.assertTrue(isinstance(logs, list))

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
