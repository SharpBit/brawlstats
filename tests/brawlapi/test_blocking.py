# import datetime
import unittest
import os
import time

import brawlstats
from brawlstats.brawlapi.models import BattleLog, Club, Constants, Events, Leaderboard, PartialClub
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

        partialclub = player.get_club(full=False)
        self.assertIsInstance(partialclub, PartialClub)
        full_club = partialclub.get_full()
        self.assertIsInstance(full_club, Club)
        club = player.get_club()
        self.assertIsInstance(club, Club)

    def test_get_club(self):
        club = self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    def test_get_leaderboard_player(self):
        lb = self.client.get_player_leaderboard(limit=200)
        self.assertIsInstance(lb, Leaderboard)
        lb = self.client.get_player_leaderboard(limit=5, region='us')
        self.assertIsInstance(lb, Leaderboard)

    def test_get_leaderboard_club(self):
        lb = self.client.get_club_leaderboard(limit=200)
        self.assertIsInstance(lb, Leaderboard)
        lb = self.client.get_club_leaderboard(limit=5, region='us')
        self.assertIsInstance(lb, Leaderboard)

    def test_get_leaderboard_brawler(self):
        lb = self.client.get_club_leaderboard('shelly', limit=200)
        self.assertIsInstance(lb, Leaderboard)
        lb = self.client.get_club_leaderboard('mortis', limit=5, region='us')
        self.assertIsInstance(lb, Leaderboard)

    def test_get_events(self):
        events = self.client.get_events()
        self.assertIsInstance(events, Events)

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertIsInstance(default, Constants)
        maps = self.client.get_constants('maps')
        self.assertIsInstance(maps, Constants)

        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    # def test_get_misc(self):
    #     misc = self.client.get_misc()
    #     self.assertEqual(misc.server_date_year, datetime.date.today().year)

    def test_club_search(self):
        search = self.client.search_club('Cactus Bandits')
        self.assertIsInstance(search, list)

    def test_battle_logs(self):
        logs = self.client.get_battle_logs(self.player_tag)
        self.assertIsInstance(logs, BattleLog)

    # Other
    def test_invalid_tag(self):
        get_player = self.client.get_player
        invalid_tag = 'P'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = '2PPPPPPP'
        self.assertRaises(brawlstats.ServerError, get_player, invalid_tag)


if __name__ == '__main__':
    unittest.main()
