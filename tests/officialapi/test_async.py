import asynctest
import asyncio
import os

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('official_token')


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
            timeout=30
        )

    async def tearDown(self):
        await asyncio.sleep(1)
        await self.client.close()

    async def test_get_player(self):
        player = await self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    async def test_get_club(self):
        club = await self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    async def test_get_club_members(self):
        members = await self.client.get_club_members(self.club_tag)
        self.assertTrue(isinstance(members, brawlstats.officialapi.Members))

    async def test_get_rankings_player(self):
        rankings = await self.client.get_rankings('players')
        self.assertTrue(isinstance(rankings, brawlstats.officialapi.Ranking))
        region = await self.client.get_rankings('players', region='us')
        self.assertTrue(isinstance(region, brawlstats.officialapi.Ranking))

    async def test_get_rankings_club(self):
        rankings = await self.client.get_rankings('clubs')
        self.assertTrue(isinstance(rankings, brawlstats.officialapi.Ranking))

    async def test_get_rankings_brawler(self):
        rankings = await self.client.get_rankings('brawlers', brawler='shelly')
        self.assertTrue(isinstance(rankings, brawlstats.officialapi.Ranking))
        rankings = await self.client.get_rankings('brawlers', brawler=16000000)
        self.assertTrue(isinstance(rankings, brawlstats.officialapi.Ranking))

    async def test_get_constants(self):
        default = await self.client.get_constants()
        self.assertTrue(isinstance(default, brawlstats.officialapi.Constants))
        maps = await self.client.get_constants('maps')
        self.assertTrue(isinstance(maps, brawlstats.officialapi.Constants))

        async def request():
            await self.get_constants(invalid_key)
        invalid_key = 'invalid'
        self.assertAsyncRaises(KeyError, request)

    async def test_battle_logs(self):
        logs = await self.client.get_battle_logs(self.player_tag)
        self.assertTrue(isinstance(logs, brawlstats.officialapi.BattleLog))

    # Other
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
            await self.client.get_rankings(invalid_type, invalid_limit)
        invalid_type = 'test'
        invalid_limit = 200
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = 'string'
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertAsyncRaises(ValueError, request)


if __name__ == '__main__':
    asynctest.main()
