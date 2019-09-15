import unittest
import os
import time

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('official_token')


class TestBlockingClient(unittest.TestCase):
    """Tests all methods in the blocking OfficialAPI client that
    uses the `requests` module in `brawlstats`
    """

    def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.club_tag = 'QCGV8PG'
        self.client = brawlstats.OfficialAPI(
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

    def test_get_club_members(self):
        members = self.client.get_club_members(self.club_tag)
        self.assertTrue(isinstance(members, brawlstats.officialapi.Members))

    def test_get_rankings_player(self):
        lb = self.client.get_rankings('players')
        self.assertTrue(isinstance(lb, brawlstats.officialapi.Ranking))
        region = self.client.get_rankings('players', region='us')
        self.assertTrue(isinstance(region, brawlstats.officialapi.Ranking))

    def test_get_rankings_club(self):
        lb = self.client.get_rankings('clubs')
        self.assertTrue(isinstance(lb, brawlstats.officialapi.Ranking))

    def test_get_rankings_brawler(self):
        lb = self.client.get_rankings('brawlers', brawler='shelly')
        self.assertTrue(isinstance(lb, brawlstats.officialapi.Ranking))

    def test_get_constants(self):
        default = self.client.get_constants()
        self.assertTrue(isinstance(default, brawlstats.officialapi.Constants))
        maps = self.client.get_constants('maps')
        self.assertTrue(isinstance(maps, brawlstats.officialapi.Constants))
        get_constants = self.client.get_constants
        invalid_key = 'invalid'
        self.assertRaises(KeyError, get_constants, invalid_key)

    def test_battle_logs(self):
        logs = self.client.get_battle_logs(self.player_tag)
        self.assertTrue(isinstance(logs, brawlstats.officialapi.BattleLog))

    # Other
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
        invalid_limit = 'string'
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertRaises(ValueError, get_rankings, invalid_type, invalid_limit)


if __name__ == '__main__':
    unittest.main()
