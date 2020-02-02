import datetime
import unittest
import os
import time

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('unofficial_token')


class TestBlockingClient(unittest.TestCase):
    """Tests all methods in the blocking BrawlAPI client that
    uses the `requests` module in `brawlstats`
    """

    def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.club_tag = 'QCGV8PG'
        self.client = brawlstats.BrawlAPI(
            TOKEN,
            is_async=False,
            timeout=30
        )

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
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))
        region = self.client.get_leaderboard('players', region='us')
        self.assertTrue(isinstance(region, brawlstats.brawlapi.Leaderboard))

    def test_get_leaderboard_club(self):
        lb = self.client.get_leaderboard('clubs')
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))

    def test_get_leaderboard_brawler(self):
        lb = self.client.get_leaderboard('brawlers', brawler='shelly')
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))

    def test_get_events(self):
        events = self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertTrue(isinstance(default, brawlstats.brawlapi.Constants))
        maps = self.client.get_constants('maps')
        self.assertTrue(isinstance(maps, brawlstats.brawlapi.Constants))
        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    def test_get_misc(self):
        misc = self.client.get_misc()
        self.assertEqual(misc.server_date_year, datetime.date.today().year)

    def test_club_search(self):
        search = self.client.search_club('Cactus Bandits')
        self.assertTrue(isinstance(search, list))

    def test_battle_logs(self):
        logs = self.client.get_battle_logs(self.player_tag)
        self.assertTrue(isinstance(logs, brawlstats.brawlapi.BattleLog))

    # Other
    def test_invalid_tag(self):
        get_player = self.client.get_player
        invalid_tag = 'P'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = '2PPPPPPP'
        self.assertRaises(brawlstats.ServerError, get_player, invalid_tag)

    def test_invalid_lb(self):
        get_lb = self.client.get_leaderboard
        invalid_type = 'test'
        invalid_limit = 200
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertRaises(ValueError, get_lb, invalid_type, invalid_limit)


if __name__ == '__main__':
    unittest.main()
