import os

import asynctest
import brawlstats
import pytest
from dotenv import load_dotenv

pytestmark = pytest.mark.asyncio
load_dotenv()


class TestAsyncClient(asynctest.TestCase):

    PLAYER_TAG = '#V2LQY9UY'
    CLUB_TAG = '#UL0GCC8'

    async def setUp(self):
        self.client = brawlstats.Client(
            os.getenv('token'),
            base_url=os.getenv('base_url'),
            is_async=True
        )

    async def tearDown(self):
        await self.client.close()

    async def test_get_player(self):
        player = await self.client.get_player(self.PLAYER_TAG)
        self.assertIsInstance(player, brawlstats.Player)
        self.assertEqual(player.tag, self.PLAYER_TAG)

        club = await player.get_club()
        self.assertIsInstance(club, brawlstats.Club)
        self.assertEqual(club.tag, self.CLUB_TAG)

        battle_logs = await player.get_battle_logs()
        self.assertIsInstance(battle_logs, brawlstats.BattleLog)

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('2PPPPPPP')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('P')

        with self.assertRaises(brawlstats.NotFoundError):
            await self.client.get_player('AAA')

    async def test_get_battle_logs(self):
        battle_logs = await self.client.get_battle_logs(self.PLAYER_TAG)
        self.assertIsInstance(battle_logs, brawlstats.BattleLog)

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

        await self.assertAsyncRaises(brawlstats.NotFoundError, self.client.get_club_members('8GGGGGGG'))

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
            await self.client.get_rankings(ranking='people', limit=0)

        with self.assertRaises(ValueError):
            await self.client.get_rankings(ranking='brawlers', brawler='SharpBit')

    async def test_get_constants(self):
        constants = await self.client.get_constants()
        self.assertIsInstance(constants, brawlstats.Constants)

        maps = await self.client.get_constants('maps')
        self.assertIsInstance(maps, brawlstats.Constants)

        await self.assertAsyncRaises(KeyError, self.client.get_constants('invalid'))

    async def test_get_brawlers(self):
        brawlers = await self.client.get_brawlers()
        self.assertIsInstance(brawlers, brawlstats.Brawlers)

    async def test_get_event_rotation(self):
        events = await self.client.get_event_rotation()
        self.assertIsInstance(events, brawlstats.EventRotation)


if __name__ == '__main__':
    asynctest.main()
