import asynctest
import os
import time

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('./.env'))

TOKEN = os.getenv('token')


class TestAsyncClient(asynctest.TestCase):
    """Tests all methods in the asynchronous client that
    uses the `aiohttp` module in `brawlstats`
    """
    async def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.band_tag = 'QCGV8PG'
        self.client = brawlstats.Client(TOKEN, is_async=True, timeout=30)

    async def tearDown(self):
        time.sleep(2)
        await self.client.close()

    async def test_get_player(self):
        player = await self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    async def test_get_band(self):
        band = await self.client.get_band(self.band_tag)
        self.assertEqual(band.tag, self.band_tag)

    async def test_get_leaderboard_player(self):
        lb = await self.client.get_leaderboard('players')
        self.assertTrue(isinstance(lb.players, list))

    async def test_get_leaderboard_band(self):
        lb = await self.client.get_leaderboard('bands')
        self.assertTrue(isinstance(lb.bands, list))

    async def test_get_events(self):
        events = await self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

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

    async def test_invalid_lb(self):
        async def request():
            await self.client.get_leaderboard(invalid_type, invalid_count)
        invalid_type = 'test'
        invalid_count = 200
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_count = 'string'
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_count = 201
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_count = -5
        self.assertAsyncRaises(ValueError, request)


if __name__ == '__main__':
    asynctest.main()