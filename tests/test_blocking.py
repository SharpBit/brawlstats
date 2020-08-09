import os
import unittest

import brawlstats
from dotenv import load_dotenv

load_dotenv()


class TestBlockingClient(unittest.TestCase):

    PLAYER_TAG = '#GGJVJLU2'
    CLUB_TAG = '#QCCQCGV'

    PLAYER_TAGS = [PLAYER_TAG, "#2Q0QL2PL"]
    CLUB_TAGS = [CLUB_TAG, "#QC0CPJRC"]

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

        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, '2PPPPPPP')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, 'P')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, 'AAA')

    def test_get_battle_logs(self):
        battle_logs = self.client.get_battle_logs(self.PLAYER_TAG)
        self.assertIsInstance(battle_logs, brawlstats.BattleLog)

        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, '2PPPPPPP')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, 'P')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_player, 'AAA')

    def test_get_club(self):
        club = self.client.get_club(self.CLUB_TAG)
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        club_members = club.get_members()
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        self.assertRaises(brawlstats.NotFoundError, self.client.get_club, '8GGGGGGG')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_club, 'P')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_club, 'AAA')

    def test_get_club_members(self):
        club_members = self.client.get_club_members(self.CLUB_TAG)
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        self.assertRaises(brawlstats.NotFoundError, self.client.get_club_members, '8GGGGGGG')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_club_members, 'P')
        self.assertRaises(brawlstats.NotFoundError, self.client.get_club_members, 'AAA')

    def test_get_rankings(self):
        player_ranking = self.client.get_rankings(ranking='players')
        self.assertIsInstance(player_ranking, brawlstats.Ranking)

        us_player_ranking = self.client.get_rankings(ranking='players', region='US', limit=1)
        self.assertIsInstance(us_player_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_player_ranking) == 1)

        club_ranking = self.client.get_rankings(ranking='clubs')
        self.assertIsInstance(club_ranking, brawlstats.Ranking)

        us_club_ranking = self.client.get_rankings(ranking='clubs', region='US', limit=1)
        self.assertIsInstance(us_club_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_club_ranking) == 1)

        brawler_ranking = self.client.get_rankings(ranking='brawlers', brawler='Shelly')
        self.assertIsInstance(brawler_ranking, brawlstats.Ranking)

        us_brawler_ranking = self.client.get_rankings(ranking='brawlers', brawler=16000000, region='US', limit=1)
        self.assertIsInstance(us_brawler_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_brawler_ranking) == 1)

        self.assertRaises(ValueError, self.client.get_rankings, ranking='people')
        self.assertRaises(ValueError, self.client.get_rankings, ranking='people', limit=0)
        self.assertRaises(ValueError, self.client.get_rankings, ranking='players', limit=201)
        self.assertRaises(ValueError, self.client.get_rankings, ranking='brawlers')
        self.assertRaises(ValueError, self.client.get_rankings, ranking='brawlers', brawler='SharpBit')
        self.assertRaises(TypeError, self.client.get_rankings, ranking='brawlers', brawler=complex())

    def test_get_constants(self):
        constants = self.client.get_constants()
        self.assertIsInstance(constants, brawlstats.Constants)

        maps = self.client.get_constants('maps')
        self.assertIsInstance(maps, brawlstats.Constants)

        self.assertRaises(KeyError, self.client.get_constants, 'invalid')

    def test_get_brawlers(self):
        brawlers = self.client.get_brawlers()
        self.assertIsInstance(brawlers, brawlstats.Brawlers)

    def test_get_players(self):
        players = self.client.get_players(self.PLAYER_TAGS)
        self.assertIsInstance(players, list)

        self.assertIsInstance(players[0], brawlstats.Player)
        self.assertIsInstance(players[1], brawlstats.Player)

        self.assertEqual(players[0].tag, self.PLAYER_TAGS[0])
        self.assertEqual(players[1].tag, self.PLAYER_TAGS[1])

        club = players[0].get_club()
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAGS[0])

        self.assertRaises(brawlstats.NotFoundError, self.client.get_players, ['2PPPPPPP'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_players, ['P'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_players, ['AAA'])

    def test_get_multiple_battle_logs(self):
        multiple_battle_logs = self.client.get_multiple_battle_logs(self.PLAYER_TAGS)
        self.assertIsInstance(multiple_battle_logs, list)
        self.assertIsInstance(multiple_battle_logs[0], brawlstats.BattleLog)
        self.assertIsInstance(multiple_battle_logs[1], brawlstats.BattleLog)

        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_battle_logs, ['2PPPPPPP'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_battle_logs, ['P'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_battle_logs, ['AAA'])

    def test_get_clubs(self):
        clubs = self.client.get_clubs(self.CLUB_TAGS)
        self.assertIsInstance(clubs, list)

        self.assertIsInstance(clubs[0], brawlstats.Club)
        self.assertIsInstance(clubs[1], brawlstats.Club)

        self.assertEqual(clubs[0].tag, self.CLUB_TAGS[0])
        self.assertEqual(clubs[1].tag, self.CLUB_TAGS[1])

        club_members = clubs[0].get_members()
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAGS[0], [x.tag for x in club_members])

        self.assertRaises(brawlstats.NotFoundError, self.client.get_clubs, ['8GGGGGGG'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_clubs, ['P'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_clubs, ['AAA'])

    def test_get_multiple_club_members(self):
        multiple_club_members = self.client.get_multiple_club_members(self.CLUB_TAGS)
        self.assertIsInstance(multiple_club_members, list)

        self.assertIsInstance(multiple_club_members[0], brawlstats.Members)
        self.assertIsInstance(multiple_club_members[1], brawlstats.Members)

        self.assertIn(self.PLAYER_TAGS[0], [x.tag for x in multiple_club_members[0]])
        self.assertIn(self.PLAYER_TAGS[1], [x.tag for x in multiple_club_members[1]])

        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_club_members, ['8GGGGGGG'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_club_members, ['P'])
        self.assertRaises(brawlstats.NotFoundError, self.client.get_multiple_club_members, ['AAA'])

    def test_get_multiple_rankings(self):
        multiple_player_ranking = self.client.get_multiple_rankings(rankings=['players'])
        self.assertIsInstance(multiple_player_ranking, list)
        self.assertIsInstance(multiple_player_ranking[0], brawlstats.Ranking)

        multiple_us_player_ranking = self.client.get_multiple_rankings(rankings=['players'], regions='US', limits=1)
        self.assertIsInstance(multiple_us_player_ranking, list)
        self.assertIsInstance(multiple_us_player_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_player_ranking[0]) == 1)

        multiple_club_ranking = self.client.get_multiple_rankings(rankings=['clubs'])
        self.assertIsInstance(multiple_club_ranking, list)
        self.assertIsInstance(multiple_club_ranking[0], brawlstats.Ranking)

        multiple_us_club_ranking = self.client.get_multiple_rankings(rankings=['clubs'], regions='US', limits=1)
        self.assertIsInstance(multiple_us_club_ranking, list)
        self.assertIsInstance(multiple_us_club_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_club_ranking[0]) == 1)

        multiple_brawler_ranking = self.client.get_multiple_rankings(rankings=['brawlers'], brawlers='Shelly')
        self.assertIsInstance(multiple_brawler_ranking, list)
        self.assertIsInstance(multiple_brawler_ranking[0], brawlstats.Ranking)

        multiple_us_brawler_ranking = self.client.get_multiple_rankings(
            rankings=['brawlers'], brawlers=16000000, regions='US', limits=1)
        self.assertIsInstance(multiple_us_brawler_ranking, list)
        self.assertIsInstance(multiple_us_brawler_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_brawler_ranking[0]) == 1)

        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['people'])
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['players'], limits=0)
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['players'], limits=201)
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['brawlers'])
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['brawlers'], brawlers='SharpBit')
        self.assertRaises(TypeError, self.client.get_multiple_rankings, rankings=['brawlers'], brawlers=complex())
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings='players')
        self.assertRaises(ValueError, self.client.get_multiple_rankings, rankings=['brawlers'], limits=[100, 200])

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
