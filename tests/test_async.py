import asynctest
import asyncio
import os

import brawlstats
from brawlstats.models import BattleLog, Club, Constants, Members, Ranking
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

TOKEN = os.getenv('token')
URL = os.getenv('base_url')


class TestAsyncClient(asynctest.TestCase):
    """Tests all methods in the asynchronous client that
    uses the `aiohttp` module in `brawlstats`
    """
    async def setUp(self):
        self.player_tag = '#GGJVJLU2'
        self.club_tag = '#QCGV8PG'
        self.client = brawlstats.Client(
            TOKEN,
            is_async=True,
            base_url=URL,
            timeout=30
        )

    async def tearDown(self):
        await asyncio.sleep(1)
        await self.client.close()

    async def test_get_player(self):
        player = await self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

        club = await player.get_club()
        self.assertIsInstance(club, Club)

    async def test_get_club(self):
        club = await self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

        members = await club.get_members()
        self.assertIsInstance(members, Members)

    async def test_get_club_members(self):
        members = await self.client.get_club_members(self.club_tag)
        self.assertIsInstance(members, Members)

    async def test_get_rankings_player(self):
        rankings = await self.client.get_rankings(ranking='players')
        self.assertIsInstance(rankings, Ranking)
        region = await self.client.get_rankings(ranking='players', region='us')
        self.assertIsInstance(region, Ranking)

    async def test_get_rankings_club(self):
        rankings = await self.client.get_rankings(ranking='clubs')
        self.assertIsInstance(rankings, Ranking)
        limit = await self.client.get_rankings(ranking='clubs', limit=100)
        self.assertTrue(len(limit) == 100)

    async def test_get_rankings_brawler(self):
        rankings = await self.client.get_rankings(ranking='brawlers', brawler='shelly')
        self.assertIsInstance(rankings, Ranking)
        rankings = await self.client.get_rankings(ranking='brawlers', brawler=16000000)
        self.assertIsInstance(rankings, Ranking)

    async def test_get_constants(self):
        default = await self.client.get_constants()
        self.assertIsInstance(default, Constants)
        maps = await self.client.get_constants('maps')
        self.assertIsInstance(maps, Constants)

        async def request():
            await self.get_constants(invalid_key)
        invalid_key = 'invalid'
        self.assertAsyncRaises(KeyError, request)

    async def test_battle_logs(self):
        logs = await self.client.get_battle_logs(self.player_tag)
        self.assertIsInstance(logs, BattleLog)

    async def test_invalid_tag(self):
        async def request():
            await self.client.get_player(invalid_tag)
        invalid_tag = 'P'
        self.assertAsyncRaises(brawlstats.NotFoundError, request)
        invalid_tag = 'AAA'
        self.assertAsyncRaises(brawlstats.NotFoundError, request)
        invalid_tag = '2PPPPPPP'
        self.assertAsyncRaises(brawlstats.NotFoundError, request)

    async def test_invalid_rankings(self):
        async def request():
            await self.client.get_rankings(ranking=invalid_ranking, limit=invalid_limit)
        invalid_ranking = 'test'
        invalid_limit = 200
        self.assertAsyncRaises(ValueError, request)
        invalid_ranking = 'players'
        invalid_limit = 201
        self.assertAsyncRaises(ValueError, request)
        invalid_ranking = 'players'
        invalid_limit = -5
        self.assertAsyncRaises(ValueError, request)


if __name__ == '__main__':
    asynctest.main()
