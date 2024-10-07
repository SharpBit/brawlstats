import asyncio
import json
import logging
import sys
from typing import Union

import aiohttp
import requests
from cachetools import TTLCache

from .errors import Forbidden, NotFoundError, RateLimitError, ServerError, UnexpectedError
from .models import BattleLog, Brawlers, Club, Constants, Members, Player, Ranking
from .utils import API, bstag, typecasted

log = logging.getLogger(__name__)


class Client:
    """A sync/async client class that lets you access the Brawl Stars API

    Parameters
    ------------
    token: str
        The API Key that you can get from https://developer.brawlstars.com
    session: Union[requests.Session, aiohttp.ClientSession], optional
        Use a current session or a make new one, by default None
    timeout: int, optional
        How long to wait in seconds before shutting down requests, by default 30
    is_async: bool, optional
        Setting this to ``True`` makes the client async, by default False
    loop: asyncio.AbstractEventLoop, optional
        The event loop to use for asynchronous operations, by default None.
        If you are passing in an aiohttp session, using this will not work:
        you must set it when initializing the session.
    connector: aiohttp.BaseConnector, optional
        Pass a Connector into the client (aiohttp), by default None
        If you are passing in an aiohttp session, using this will not work:
        you must set it when initializing the session.
    debug: bool, optional
        Whether or not to log info for debugging, by default False
    base_url: str, optional
        Sets a different base URL to make request to, by default None
    """

    REQUEST_LOG = '{method} {url} recieved {text} has returned {status}'

    def __init__(self, token, session=None, timeout=30, is_async=False, **options):
        # Async options
        self.is_async = is_async
        self.loop = options.get('loop', asyncio.get_event_loop()) if self.is_async else None
        self.connector = options.get('connector')

        self.debug = options.get('debug', False)
        self.cache = TTLCache(3200 * 3, 60 * 3)  # 3200 requests per minute

        # Session and request options
        self.session = session or (
            aiohttp.ClientSession(loop=self.loop, connector=self.connector) if self.is_async else requests.Session()
        )
        self.timeout = timeout
        self.prevent_ratelimit = options.get('prevent_ratelimit', False)
        if self.is_async and self.prevent_ratelimit:
            self.lock = asyncio.Lock(loop=self.loop)
        self.api = API(base_url=options.get('base_url'), version=1)

        # Request/response headers
        self.headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': f'brawlstats/{self.api.VERSION} (Python {sys.version_info[0]}.{sys.version_info[1]})',
            'Accept-Encoding': 'gzip'
        }

        # Load brawlers for get_rankings
        if self.is_async:
            self.loop.create_task(self._ainit())
        else:
            brawlers_info = self.get_brawlers()
            self.api.set_brawlers(brawlers_info)

    async def _ainit(self):
        """Task created to run `get_brawlers` asynchronously"""
        self.api.set_brawlers(await self.get_brawlers())

    def __repr__(self):
        return f'<Client async={self.is_async} timeout={self.timeout} debug={self.debug}>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        return self.session.close()

    def _raise_for_status(self, resp, text):
        """
        Checks for invalid error codes returned by the API.
        """
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text

        code = getattr(resp, 'status', None) or getattr(resp, 'status_code')
        url = resp.url

        if self.debug:
            log.debug(self.REQUEST_LOG.format(method='GET', url=url, text=text, status=code))

        if 300 > code >= 200:
            return data
        if code == 403:
            raise Forbidden(code, url, data['message'])
        if code == 404:
            raise NotFoundError(code, reason='Resource not found.')
        if code == 429:
            raise RateLimitError(code, url)
        if code == 500:
            raise UnexpectedError(code, url, data)
        if code == 503:
            raise ServerError(code, url)

    def _resolve_cache(self, url):
        """Find any cached response for the same requested url."""
        data = self.cache.get(url)
        if not data:
            return None
        if self.debug:
            log.debug(f'GET {url} got result from cache.')
        return data

    async def _arequest(self, url, use_cache=True):
        """Async method to request a url."""
        # Try and retrieve from cache
        if use_cache:
            cache = self._resolve_cache(url)
        else:
            cache = None

        if cache is not None:
            return cache

        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                data = self._raise_for_status(resp, await resp.text())
        except asyncio.TimeoutError:
            raise ServerError(503, url)
        else:
            # Cache the data if successful
            self.cache[url] = data

        return data

    def _request(self, url, use_cache=True):
        """Sync method to request a url."""
        if self.is_async:
            return self._arequest(url, use_cache=use_cache)

        # Try and retrieve from cache
        if use_cache:
            cache = self._resolve_cache(url)
        else:
            cache = None
        if cache is not None:
            return cache

        try:
            with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                data = self._raise_for_status(resp, resp.text)
        except requests.Timeout:
            raise ServerError(503, url)
        else:
            # Cache the data if successful
            self.cache[url] = data

        return data

    async def _aget_model(self, url, model, use_cache=True, key=None):
        """Method to turn the response data into a Model class for the async client."""
        data = await self._arequest(url, use_cache=use_cache)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError(f'No such Constants key "{key}"')

        return model(self, data)

    def _get_model(self, url, model, use_cache=True, key=None):
        """Method to turn the response data into a Model class for the sync client."""
        if self.is_async:
            # Calls the async function
            return self._aget_model(url, model=model, use_cache=use_cache, key=key)

        data = self._request(url, use_cache)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError(f'No such Constants key "{key}"')

        return model(self, data)

    @typecasted
    def get_player(self, tag: bstag, use_cache=True) -> Player:
        """Gets a player's stats.

        Parameters
        ----------
        tag : str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Player
            A player object with all of its attributes.
        """
        url = f'{self.api.PROFILE}/{tag}'
        return self._get_model(url, model=Player, use_cache=use_cache)

    get_profile = get_player

    @typecasted
    def get_battle_logs(self, tag: bstag, use_cache=True) -> BattleLog:
        """Gets a player's battle logs.

        Parameters
        ----------
        tag : str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        BattleLog
            A player battle object with all of its attributes.
        """
        url = f'{self.api.PROFILE}/{tag}/battlelog'
        return self._get_model(url, model=BattleLog, use_cache=use_cache)

    @typecasted
    def get_club(self, tag: bstag, use_cache=True) -> Club:
        """Gets a club's stats.

        Parameters
        ----------
        tag : str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Club
            A club object with all of its attributes.
        """
        url = f'{self.api.CLUB}/{tag}'
        return self._get_model(url, model=Club, use_cache=use_cache)

    @typecasted
    def get_club_members(self, tag: bstag, use_cache=True) -> Members:
        """Gets the members of a club.

        Parameters
        ----------
        tag : str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Members
            A list of the members in a club.
        """
        url = f'{self.api.CLUB}/{tag}/members'
        return self._get_model(url, model=Members, use_cache=use_cache)

    def get_rankings(
        self, *, ranking: str, region: str=None, limit: int=200,
        brawler: Union[str, int]=None, use_cache=True
    ) -> Ranking:
        """Gets the top count players/clubs/brawlers.

        Parameters
        ----------
        ranking : str
            The type of ranking. Must be "players", "clubs", "brawlers".
        region : str, optional
            The region to retrieve from. Must be a 2 letter country code, 'global', or None: by default None
        limit : int, optional
            The number of top players or clubs to fetch, by default 200
        brawler : Union[str, int], optional
            The brawler name or ID, by default None
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Ranking
            A player or club ranking that contains a list of players or clubs.

        Raises
        ------
        ValueError
            The brawler name or ID is invalid.
        ValueError
            `rankings` is not "players", "clubs", or "brawlers"
        ValueError
            `limit` is not between 1 and 200, inclusive.
        """
        if brawler is not None:
            if isinstance(brawler, str):
                brawler = brawler.lower()

            # Replace brawler name with ID
            if brawler in self.api.CURRENT_BRAWLERS.keys():
                brawler = self.api.CURRENT_BRAWLERS[brawler]

            if brawler not in self.api.CURRENT_BRAWLERS.values():
                raise ValueError('Invalid brawler.')

        if region is None:
            region = 'global'

        # Check for invalid parameters
        if ranking not in ('players', 'clubs', 'brawlers'):
            raise ValueError("'ranking' must be 'players', 'clubs' or 'brawlers'.")
        if not 0 < limit <= 200:
            raise ValueError('Make sure limit is between 1 and 200.')

        # Construct URL
        url = f'{self.api.RANKINGS}/{region}/{ranking}?limit={limit}'
        if ranking == 'brawlers':
            url = f'{self.api.RANKINGS}/{region}/{ranking}/{brawler}?limit={limit}'

        return self._get_model(url, model=Ranking, use_cache=use_cache)

    def get_constants(self, key: str=None, use_cache=True) -> Constants:
        """Gets Brawl Stars constants extracted from the app.

        Parameters
        ----------
        key : str, optional
            Any key to get specific data, by default None
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Constants
            Data containing some Brawl Stars constants.
        """
        return self._get_model(self.api.CONSTANTS, model=Constants, key=key, use_cache=use_cache)

    def get_brawlers(self, use_cache=True) -> Brawlers:
        """Gets available brawlers and information about them.

        Parameters
        ----------
        use_cache : bool, optional
            Whether to use the internal 3 minutes cache, by default True

        Returns
        -------
        Brawlers
            A list of available brawlers and information about them.
        """
        return self._get_model(self.api.BRAWLERS, model=Brawlers, use_cache=use_cache)
