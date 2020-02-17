import unittest
import os
import time

import brawlstats
from brawlstats.officialapi.models import BattleLog, Club, Constants, Members, Ranking
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('official_token')
URL = os.getenv('official_api_url')


class TestBlockingClient(unittest.TestCase):
    """Tests all methods in the blocking OfficialAPI client that
    uses the `requests` module in `brawlstats`
    """

    def setUp(self):
        self.player_tag = '#GGJVJLU2'
        self.club_tag = '#QCGV8PG'
        self.client = brawlstats.OfficialAPI(
            TOKEN,
            is_async=False,
            base_url=URL,
            timeout=30
        )

    def tearDown(self):
        time.sleep(1)
        self.client.close()

    def test_get_player(self):
        player = self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

        club = player.get_club()
        self.assertIsInstance(club, Club)

    def test_get_club(self):
        club = self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

        members = club.get_members()
        self.assertIsInstance(members, Members)

    def test_get_club_members(self):
        members = self.client.get_club_members(self.club_tag)
        self.assertIsInstance(members, Members)

    def test_get_rankings_player(self):
        rankings = self.client.get_rankings('players')
        self.assertIsInstance(rankings, Ranking)
        region = self.client.get_rankings('players', region='us')
        self.assertIsInstance(region, Ranking)

    def test_get_rankings_club(self):
        rankings = self.client.get_rankings('clubs')
        self.assertIsInstance(rankings, Ranking)

    def test_get_rankings_brawler(self):
        rankings = self.client.get_rankings('brawlers', brawler='shelly')
        self.assertIsInstance(rankings, Ranking)
        rankings = self.client.get_rankings('brawlers', brawler=16000000)
        self.assertIsInstance(rankings, Ranking)

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertIsInstance(default, Constants)
        maps = self.client.get_constants('maps')
        self.assertIsInstance(maps, Constants)
        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    def test_battle_logs(self):
        logs = self.client.get_battle_logs(self.player_tag)
        self.assertIsInstance(logs, BattleLog)

    def test_invalid_tag(self):
        get_player = self.client.get_player
        invalid_tag = 'P'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)
        invalid_tag = '2PPPPPPP'
        self.assertRaises(brawlstats.NotFoundError, get_player, invalid_tag)

    def test_invalid_rankings(self):
        get_rankings = self.client.get_rankings
        invalid_type = 'test'
        invalid_limit = 200
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)


if __name__ == '__main__':
    unittest.main()
