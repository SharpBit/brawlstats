import asynctest
import asyncio
import datetime
import os

import brawlstats
from brawlstats.brawlapi.models import BattleLog, Club, Constants, Events, Leaderboard, PartialClub
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('unofficial_token')


class TestAsyncClient(asynctest.TestCase):
    """Tests all methods in the asynchronous BrawlAPI client that
    uses the `aiohttp` module in `brawlstats`
    """
    async def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.club_tag = 'QCGV8PG'
        self.client = brawlstats.BrawlAPI(
            token=TOKEN,
            is_async=True,
            timeout=30
        )

    async def tearDown(self):
        await asyncio.sleep(1)
        await self.client.close()

    async def test_get_player(self):
        """Test everything relating to the Player model"""
        player = await self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

        partialclub = await player.get_club(full=False)
        self.assertIsInstance(partialclub, PartialClub)
        full_club = await partialclub.get_full()
        self.assertIsInstance(full_club, Club)
        club = await player.get_club()
        self.assertIsInstance(club, Club)

    async def test_get_club(self):
        club = await self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    async def test_get_leaderboard_player(self):
        lb = await self.client.get_leaderboard('players')
        self.assertIsInstance(lb, Leaderboard)
        lb = await self.client.get_leaderboard('players', region='us')
        self.assertIsInstance(lb, Leaderboard)
        lb = await self.client.get_leaderboard('players', region='us', limit=5)
        self.assertTrue(len(lb) == 5)

    async def test_get_leaderboard_club(self):
        lb = await self.client.get_leaderboard('clubs')
        self.assertIsInstance(lb, Leaderboard)

    async def test_get_leaderboard_brawler(self):
        lb = await self.client.get_leaderboard('brawlers', brawler='shelly')
        self.assertIsInstance(lb, Leaderboard)

    async def test_get_events(self):
        events = await self.client.get_events()
        self.assertIsInstance(events, Events)

    async def test_get_constants(self):
        default = await self.client.get_constants()
        self.assertIsInstance(default, Constants)
        maps = await self.client.get_constants('maps')
        self.assertIsInstance(maps, Constants)

        async def request():
            await self.get_constants(invalid_key)
        invalid_key = 'invalid'
        self.assertRaises(KeyError, request)

    async def test_get_misc(self):
        misc = await self.client.get_misc()
        self.assertEqual(misc.server_date_year, datetime.date.today().year)

    async def test_club_search(self):
        search = await self.client.search_club('Cactus Bandits')
        self.assertIsInstance(search, list)

    async def test_battle_logs(self):
        logs = await self.client.get_battle_logs(self.player_tag)
        self.assertIsInstance(logs, BattleLog)

    async def test_invalid_tag(self):
        async def request():
            await self.client.get_player(invalid_tag)
        invalid_tag = 'P'
        self.assertRaises(brawlstats.NotFoundError, request)
        invalid_tag = 'AAA'
        self.assertRaises(brawlstats.NotFoundError, request)
        invalid_tag = '2PPPPPPP'
        self.assertRaises(brawlstats.ServerError, request)

    async def test_invalid_lb(self):
        async def request():
            await self.client.get_leaderboard(invalid_type, invalid_limit)
        invalid_type = 'test'
        invalid_limit = 200
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertAsyncRaises(ValueError, request)


if __name__ == '__main__':
    asynctest.main()
