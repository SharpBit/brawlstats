import os
import unittest

import brawlstats
from dotenv import load_dotenv

load_dotenv()


class TestBlockingClient(unittest.TestCase):

    PLAYER_TAG = '#GGJVJLU2'
    CLUB_TAG = '#QCCQCGV'

    def setUp(self):

        self.client = brawlstats.Client(
            os.getenv('token'),
            base_url=os.getenv('base_url')
        )

    def test_get_player(self):
        player = self.client.get_player(self.PLAYER_TAG)
        self.assertIsInstance(player, brawlstats.Player)
        self.assertEqual(player.tag, self.PLAYER_TAG)

        club = player.get_club()
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_player, '2PPPPPPP')
        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_player, 'P')
        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_player, 'AAA')

    def test_get_battle_logs(self):
        battle_logs = self.client.get_battle_logs(self.PLAYER_TAG)
        self.assertIsInstance(battle_logs, brawlstats.BattleLog)

    def test_get_club(self):
        club = self.client.get_club(self.CLUB_TAG)
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        club_members = club.get_members()
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_club, '8GGGGGGG')
        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_club, 'P')
        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_club, 'AAA')

    def test_get_club_members(self):
        club_members = self.client.get_club_members(self.CLUB_TAG)
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        self.assertRaises(
            brawlstats.NotFoundError, self.client.get_club_members, '8GGGGGGG')

    def test_get_rankings(self):
        player_ranking = self.client.get_rankings(ranking='players')
        self.assertIsInstance(player_ranking, brawlstats.Ranking)

        us_player_ranking = self.client.get_rankings(
            ranking='players', region='US', limit=1)
        self.assertIsInstance(us_player_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_player_ranking) == 1)

        self.assertRaises(
            ValueError, self.client.get_rankings, ranking='people')
        self.assertRaises(
            ValueError, self.client.get_rankings, ranking='people', limit=0)
        self.assertRaises(
            ValueError, self.client.get_rankings,
            ranking='brawlers', brawler='SharpBit')

        club_ranking = self.client.get_rankings(ranking='clubs')
        self.assertIsInstance(club_ranking, brawlstats.Ranking)

        us_club_ranking = self.client.get_rankings(
            ranking='clubs', region='US', limit=1)
        self.assertIsInstance(us_club_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_club_ranking) == 1)

        brawler_ranking = self.client.get_rankings(
            ranking='brawlers', brawler='Shelly')
        self.assertIsInstance(brawler_ranking, brawlstats.Ranking)

        us_brawler_ranking = self.client.get_rankings(
            ranking='brawlers', brawler=16000000, region='US', limit=1)
        self.assertIsInstance(us_brawler_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_brawler_ranking) == 1)

    def test_get_constants(self):
        constants = self.client.get_constants()
        self.assertIsInstance(constants, brawlstats.Constants)

        maps = self.client.get_constants('maps')
        self.assertIsInstance(maps, brawlstats.Constants)

        self.assertRaises(KeyError, self.client.get_constants, 'invalid')

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
