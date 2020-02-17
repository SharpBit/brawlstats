import asynctest
import asyncio
import os

import brawlstats
from brawlstats.officialapi.models import BattleLog, Club, Constants, Members, Ranking
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('official_token')
URL = os.getenv('official_api_url')


class TestAsyncClient(asynctest.TestCase):
    """Tests all methods in the asynchronous OfficialAPI client that
    uses the `aiohttp` module in `brawlstats`
    """
    async def setUp(self):
        self.player_tag = '#GGJVJLU2'
        self.club_tag = '#QCGV8PG'
        self.client = brawlstats.OfficialAPI(
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
        rankings = await self.client.get_player_rankings(limit=200)
        self.assertIsInstance(rankings, Ranking)
        rankings = await self.client.get_player_rankings(limit=5, region='us')
        self.assertIsInstance(rankings, Ranking)

    async def test_get_rankings_club(self):
        rankings = await self.client.get_club_rankings(limit=200)
        self.assertIsInstance(rankings, Ranking)
        rankings = await self.client.get_club_rankings(limit=5, region='us')
        self.assertIsInstance(rankings, Ranking)

    async def test_get_rankings_brawler(self):
        rankings = await self.client.get_brawler_rankings(brawler='shelly', limit=200)
        self.assertIsInstance(rankings, Ranking)
        rankings = await self.client.get_brawler_rankings(brawler=16000000, limit=5, region='us')
        self.assertIsInstance(rankings, Ranking)

    async def test_get_constants(self):
        default = await self.client.get_constants()
        self.assertIsInstance(default, Constants)
        maps = await self.client.get_constants('maps')
        self.assertIsInstance(maps, Constants)

        async def request():
            await self.get_constants(invalid_key)
        invalid_key = 'invalid'
        self.assertRaises(KeyError, request)

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
        self.assertRaises(brawlstats.NotFoundError, request)


if __name__ == '__main__':
    asynctest.main()
