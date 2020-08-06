import os

import aiohttp
import asynctest
import brawlstats
import pytest
from dotenv import load_dotenv

pytestmark = pytest.mark.asyncio
load_dotenv()


class TestAsyncClient(asynctest.TestCase):
    use_default_loop = True

    PLAYER_TAG = '#GGJVJLU2'
    CLUB_TAG = '#QCCQCGV'

    PLAYER_TAGS = [PLAYER_TAG, "#2Q0QL2PL"]
    CLUB_TAGS = [CLUB_TAG, "#QC0CPJRC"]

    async def setUp(self):
        session = aiohttp.ClientSession(loop=self.loop)

        self.client = brawlstats.Client(
            os.getenv('token'),
            base_url=os.getenv('base_url'),
            is_async=True,
            session=session
        )

    async def test_get_player(self):
        player = await self.client.get_player(self.PLAYER_TAG)
        self.assertIsInstance(player, brawlstats.Player)
        self.assertEqual(player.tag, self.PLAYER_TAG)

        club = await player.get_club()
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('2PPPPPPP')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('P')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('AAA')

    async def test_get_battle_logs(self):
        battle_logs = await self.client.get_battle_logs(self.PLAYER_TAG)
        self.assertIsInstance(battle_logs, brawlstats.BattleLog)

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_battle_logs('8GGGGGGG')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_battle_logs('P')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_battle_logs('AAA')

    async def test_get_club(self):
        club = await self.client.get_club(self.CLUB_TAG)
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        club_members = await club.get_members()
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club('8GGGGGGG')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club('P')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club('AAA')

    async def test_get_club_members(self):
        club_members = await self.client.get_club_members(self.CLUB_TAG)
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAG, [x.tag for x in club_members])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club_members('8GGGGGGG')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club_members('P')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_club_members('AAA')

    async def test_get_rankings(self):
        player_ranking = await self.client.get_rankings(ranking='players')
        self.assertIsInstance(player_ranking, brawlstats.Ranking)

        us_player_ranking = await self.client.get_rankings(ranking='players', region='US', limit=1)
        self.assertIsInstance(us_player_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_player_ranking) == 1)

        club_ranking = await self.client.get_rankings(ranking='clubs')
        self.assertIsInstance(club_ranking, brawlstats.Ranking)

        us_club_ranking = await self.client.get_rankings(ranking='clubs', region='US', limit=1)
        self.assertIsInstance(us_club_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_club_ranking) == 1)

        brawler_ranking = await self.client.get_rankings(ranking='brawlers', brawler='Shelly')
        self.assertIsInstance(brawler_ranking, brawlstats.Ranking)

        us_brawler_ranking = await self.client.get_rankings(ranking='brawlers', brawler=16000000, region='US', limit=1)
        self.assertIsInstance(us_brawler_ranking, brawlstats.Ranking)
        self.assertTrue(len(us_brawler_ranking) == 1)

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='people')

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='players', limit=0)

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='players', limit=201)

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='brawlers')

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='brawlers', brawler='SharpBit')

        with self.assertRaises(TypeError):
            await self.client.get_rankings(ranking='brawlers', brawler=complex())

    async def test_get_constants(self):
        constants = await self.client.get_constants()
        self.assertIsInstance(constants, brawlstats.Constants)

        maps = await self.client.get_constants('maps')
        self.assertIsInstance(maps, brawlstats.Constants)

        await self.assertAsyncRaises(KeyError, self.client.get_constants('invalid'))

    async def test_get_brawlers(self):
        brawlers = await self.client.get_brawlers()
        self.assertIsInstance(brawlers, brawlstats.Brawlers)

    async def test_get_players(self):
        players = await self.client.get_players(self.PLAYER_TAGS)
        self.assertIsInstance(players, list)

        self.assertIsInstance(players[0], brawlstats.Player)
        self.assertIsInstance(players[1], brawlstats.Player)

        self.assertEqual(players[0].tag, self.PLAYER_TAGS[0])
        self.assertEqual(players[1].tag, self.PLAYER_TAGS[1])

        club = await players[0].get_club()
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAGS[0])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_players(['2PPPPPPP'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_players(['P'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_players(['AAA'])

        with self.assertRaises(ValueError):
            await self.client.get_players([])

    async def test_get_multiple_battle_logs(self):
        multiple_battle_logs = await self.client.get_multiple_battle_logs(self.PLAYER_TAGS)
        self.assertIsInstance(multiple_battle_logs, list)
        self.assertIsInstance(multiple_battle_logs[0], brawlstats.BattleLog)
        self.assertIsInstance(multiple_battle_logs[1], brawlstats.BattleLog)

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_battle_logs(['2PPPPPPP'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_battle_logs(['P'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_battle_logs(['AAA'])

        with self.assertRaises(ValueError):
            await self.client.get_multiple_battle_logs([])

    async def test_get_clubs(self):
        clubs = await self.client.get_clubs(self.CLUB_TAGS)
        self.assertIsInstance(clubs, list)

        self.assertIsInstance(clubs[0], brawlstats.Club)
        self.assertIsInstance(clubs[1], brawlstats.Club)

        self.assertEqual(clubs[0].tag, self.CLUB_TAGS[0])
        self.assertEqual(clubs[1].tag, self.CLUB_TAGS[1])

        club_members = await clubs[0].get_members()
        self.assertIsInstance(club_members, brawlstats.Members)
        self.assertIn(self.PLAYER_TAGS[0], [x.tag for x in club_members])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_clubs(['8GGGGGGG'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_clubs(['P'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_clubs(['AAA'])

        with self.assertRaises(ValueError):
            await self.client.get_clubs([])

    async def test_get_multiple_club_members(self):
        multiple_club_members = await self.client.get_multiple_club_members(self.CLUB_TAGS)
        self.assertIsInstance(multiple_club_members, list)

        self.assertIsInstance(multiple_club_members[0], brawlstats.Members)
        self.assertIsInstance(multiple_club_members[1], brawlstats.Members)

        self.assertIn(self.PLAYER_TAGS[0], [x.tag for x in multiple_club_members[0]])
        self.assertIn(self.PLAYER_TAGS[1], [x.tag for x in multiple_club_members[1]])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_club_members(['8GGGGGGG'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_club_members(['P'])

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_multiple_club_members(['AAA'])

        with self.assertRaises(ValueError):
            await self.client.get_multiple_club_members([])

    async def test_get_multiple_rankings(self):
        multiple_player_ranking = await self.client.get_multiple_rankings(rankings=['players'])
        self.assertIsInstance(multiple_player_ranking, list)
        self.assertIsInstance(multiple_player_ranking[0], brawlstats.Ranking)

        multiple_us_player_ranking = await self.client.get_multiple_rankings(
            rankings=['players'], regions='US', limits=1)
        self.assertIsInstance(multiple_us_player_ranking, list)
        self.assertIsInstance(multiple_us_player_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_player_ranking[0]) == 1)

        multiple_club_ranking = await self.client.get_multiple_rankings(rankings=['clubs'])
        self.assertIsInstance(multiple_club_ranking, list)
        self.assertIsInstance(multiple_club_ranking[0], brawlstats.Ranking)

        multiple_us_club_ranking = await self.client.get_multiple_rankings(rankings=['clubs'], regions='US', limits=1)
        self.assertIsInstance(multiple_us_club_ranking, list)
        self.assertIsInstance(multiple_us_club_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_club_ranking[0]) == 1)

        multiple_brawler_ranking = await self.client.get_multiple_rankings(rankings=['brawlers'], brawlers='Shelly')
        self.assertIsInstance(multiple_brawler_ranking, list)
        self.assertIsInstance(multiple_brawler_ranking[0], brawlstats.Ranking)

        multiple_us_brawler_ranking = await self.client.get_multiple_rankings(
            rankings=['brawlers'], brawlers=16000000, regions='US', limits=1)
        self.assertIsInstance(multiple_us_brawler_ranking, list)
        self.assertIsInstance(multiple_us_brawler_ranking[0], brawlstats.Ranking)
        self.assertTrue(len(multiple_us_brawler_ranking[0]) == 1)

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['people'])

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['players'], limits=0)

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['players'], limits=201)

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['brawlers'])

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['brawlers'], brawlers='SharpBit')

        with self.assertRaises(TypeError):
            await self.client.get_multiple_rankings(rankings=['brawlers'], brawlers=complex())

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings='players')

        with self.assertRaises(ValueError):
            await self.client.get_multiple_rankings(rankings=['brawlers'], limits=[100, 200])

    async def asyncTearDown(self):
        await self.client.close()


if __name__ == '__main__':
    asynctest.main()
