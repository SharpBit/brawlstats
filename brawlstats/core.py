import asyncio
# import json
import logging
import sys
import time

import aiohttp
import requests
from cachetools import TTLCache

from .errors import IncorrectDataError, Forbidden, NotFoundError, RateLimitError, ServerError, UnexpectedError
from .models import BattleLog, Brawlers, Club, Constants, Members, Player, Ranking
from .utils import API, bstag, bstags, isiter, isstr, not_unique, typecasted, same

log = logging.getLogger(__name__)


class Client:
    """
    This is a sync/async client class that lets you access the Brawl Stars API

    Parameters
    ------------
    token: str
        The API Key that you can get from https://developer.brawlstars.com
    timeout: Optional[int] = 30
        How long to wait in seconds before shutting down requests.
    is_async: Optional[bool] = False
        Setting this to ``True`` makes the client async. Default is ``False``
    session: Optional[Union[requests.Session, aiohttp.ClientSession]] = None
        Use a current session or a make new one.
    loop: Optional[asyncio.window_events._WindowsSelectorEventLoop]
        The event loop to use for asynchronous operations. Defaults to ``None``,
        in which case the default event loop is ``asyncio.get_event_loop()``.
    connector: Optional[aiohttp.TCPConnector]
        Pass a TCPConnector into the client (aiohttp). Defaults to ``None``.
    debug: Optional[bool] = False
        Whether or not to log info for debugging.
    base_url: Optional[str] = None
        Sets a different base URL to make request to.
    return_raw_data: Optional[bool] = False
        If ``True``, then it returns raw data without using models,
        functions work about 2 times faster with async than if ``False``
    limiter Optional
        Any object that has `acquire` and `release` functions,
        such as ``asyncio.Semaphore``, ``asyncio.Lock`` and the like.
        Used to limit the number of requests and avoid being ratelimited.
        Works only if `is_async` is ``True``
        Default is ``asyncio.Semaphore``
    ratelimit Optional[float] = 15.
        If `limiter` not set then ``asyncio.Semaphore`` `value`.
        https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore
    use_limiter Optional[bool] = `is_async`
        If ``False``, then the `limiter` is not used for requests (see `limiter`)
    wait_between Optional[bool] = `is_async`
        Always wait between requests `waiting_time` to avoid being ratelimited.
    waiting_time: Optional[float] = 0.
        Timeout in seconds between requests, works if `wait_between` is ``True``
    prevent_ratelimit: Optional[bool] = `is_async`
        If True, overrides `use_limiter` and `wait_between` as True
    """

    REQUEST_LOG = '{method} {url} recieved {text} has returned {status}'

    def __init__(self, token, session=None, timeout=30, is_async=False, **options):
        # Async options
        self.is_async = is_async
        self.loop = options.get('loop', asyncio.get_event_loop()) if self.is_async else None
        self.connector = options.get('connector')

        self.debug = options.get('debug', False)
        self.cache = TTLCache(3200 * 3, 60 * 3)  # 3200 requests per minute

        # Use models or return raw data
        self.return_raw_data = options.get('return_raw_data', False)

        # Session and request options
        self.session = options.get('session') or (
            aiohttp.ClientSession(loop=self.loop, connector=self.connector) if self.is_async else requests.Session()
        )
        self.timeout = timeout
        self.api = API(base_url=options.get('base_url'), version=1)

        # handling ratelimits
        if options.get('prevent_ratelimit', self.is_async):
            self.use_limiter = self.wait_between = True
        else:
            self.use_limiter = options.get('use_limiter', False)
            self.wait_between = options.get('wait_between', False)
        self.waiting_time = options.get('waiting_time', 0)
        self.limiter = options.get('limiter') or asyncio.Semaphore(options.get('ratelimit', 15), loop=self.loop)
        # limiter = asyncio.Lock(loop=self.loop)

        # Request/response headers
        self.headers = {
            'Authorization': 'Bearer {}'.format(token),
            'User-Agent': 'brawlstats/{0} (Python {1[0]}.{1[1]})'.format(self.api.VERSION, sys.version_info),
            'Accept-Encoding': 'gzip'
        }

        # Load brawlers for get_rankings
        if self.is_async:
            self.loop.create_task(self.__ainit__())
        else:
            brawlers_info = self.get_brawlers()
            self.api.set_brawlers(brawlers_info)

    async def __ainit__(self):
        """Task created to run `get_brawlers` asynchronously"""
        self.api.set_brawlers(await self.get_brawlers())

    def __repr__(self):
        return '<Client async={} timeout={} debug={}>'.format(self.is_async, self.timeout, self.debug)

    def close(self):
        return self.session.close()

    def _raise_for_status(self, resp, text, data):
        """
        Checks for invalid error codes returned by the API.
        """
        code = getattr(resp, 'status', None) or getattr(resp, 'status_code')
        url = resp.url

        if self.debug:
            log.debug(self.REQUEST_LOG.format(method='GET', url=url, text=text, status=code))

        if 300 > code >= 200:
            return data
        if code == 400:
            raise IncorrectDataError(code, url, data['message'])
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
            log.debug('GET {} got result from cache.'.format(url))
        return data

    async def _handle_arequest(self, url):
        """Async method for handling requests to avoid rate limiting"""
        if self.use_limiter:
            async with self.limiter:
                data = await self._arequest(url)
        else:
            data = await self._arequest(url)

        if self.wait_between:
            await asyncio.sleep(self.waiting_time)

        return data

    async def _arequest(self, url):
        """Async method to request a url."""
        # Try and retrieve from cache
        cache = self._resolve_cache(url)
        if cache is not None:
            return cache

        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                data = self._raise_for_status(resp, await resp.text(), await resp.json())
        except asyncio.TimeoutError:
            raise ServerError(503, url)
        else:
            # Cache the data if successful
            self.cache[url] = data

        return data

    def _handle_request(self, url):
        """Sync method for handling requests to avoid rate limiting"""
        data = self._request(url)
        if self.wait_between:
            time.sleep(self.waiting_time)

        return data

    def _request(self, url):
        """Sync method to request a url."""
        # Try and retrieve from cache
        cache = self._resolve_cache(url)
        if cache is not None:
            return cache

        try:
            with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                data = self._raise_for_status(resp, resp.text, resp.json())
        except requests.Timeout:
            raise ServerError(503, url)
        else:
            # Cache the data if successful
            self.cache[url] = data

        return data

    def _handle_model(self, model, data):
        """Method for handling returning data"""
        if self.return_raw_data:
            items = data.get("items")
            if items is not None:
                return items
            else:
                return data
        else:
            return model(self, data)

    async def _aget_model(self, url, model, key=None):
        """Method to turn the response data into a Model class for the async client."""
        data = await self._handle_arequest(url)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError('No such Constants key "{}"'.format(key))

        return self._handle_model(model, data)

    def _get_model(self, url, model, key=None):
        """Method to turn the response data into a Model class for the sync client."""
        if self.is_async:
            # Calls the async function
            return self._aget_model(url, model=model, key=key)

        data = self._handle_request(url)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError('No such Constants key "{}"'.format(key))

        return self._handle_model(model, data)

    def _handle_models(self, model, data_list):
        """Method for handling multiple returning data"""
        if self.return_raw_data:
            for i, data in enumerate(data_list):
                items = data.get("items")
                if items is not None:
                    data_list[i] = items
                else:
                    data_list[i] = data
            return data_list
        else:
            return [model(self, data) for data in data_list]

    async def _aget_models(self, urls, model):
        """
        Method to get multiple responses and
        turn it into a Model class for the async client.
        """
        # create tasks
        tasks = [asyncio.ensure_future(self._handle_arequest(url)) for url in urls]

        # await all tasks
        data_list = await asyncio.gather(*tasks)

        return self._handle_models(model, data_list)

    def _get_models(self, urls, model):
        """
        Method to get multiple responses and
        turn it into a Model class for the sync client.
        """
        # check the uniqueness of all urls
        if len(urls) > 1 and not_unique(urls):
            raise ValueError("not all arguments in iterable are unique")

        if self.is_async:
            # Calls the async function
            return self._aget_models(urls, model=model)

        # make requests
        data_list = [self._handle_request(url) for url in urls]

        return self._handle_models(model, data_list)

    @typecasted
    def get_player(self, tag: bstag):
        """
        Get a player's stats.

        Parameters
        ----------
        tag: str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Player
        """
        url = '{}/{}'.format(self.api.PROFILE, tag)
        return self._get_model(url, model=Player)

    get_profile = get_player

    @typecasted
    def get_players(self, tags: bstags):
        """
        Get a multiple player's stats.

        Parameters
        ----------
        tags: list of tags
            A list of valid player tags.
            Player tags must be str.
            Valid characters: 0289PYLQGRJCUV

        Returns list of Player
        """
        urls = ['{}/{}'.format(self.api.PROFILE, tag) for tag in tags]
        return self._get_models(urls, model=Player)

    get_profiles = get_players

    @typecasted
    def get_battle_logs(self, tag: bstag):
        """Get a player's battle logs.

        Parameters
        ----------
        tag: str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV

        Returns BattleLog
        """
        url = '{}/{}/battlelog'.format(self.api.PROFILE, tag)
        return self._get_model(url, model=BattleLog)

    @typecasted
    def get_multiple_battle_logs(self, tags: bstags):
        """Get a multiple player's battle logs.

        Parameters
        ----------
        tags: list of tags
            A list of valid player tags.
            Player tags must be str.
            Valid characters: 0289PYLQGRJCUV

        Returns list of BattleLog
        """
        urls = ['{}/{}/battlelog'.format(self.api.PROFILE, tag) for tag in tags]
        return self._get_models(urls, model=BattleLog)

    @typecasted
    def get_club(self, tag: bstag):
        """
        Get a club's stats.

        Parameters
        ----------
        tag: str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Club
        """
        url = '{}/{}'.format(self.api.CLUB, tag)
        return self._get_model(url, model=Club)

    @typecasted
    def get_clubs(self, tags: bstags):
        """
        Get a multiple club's stats.

        Parameters
        ----------
        tags: list of tags
            A list of valid player tags.
            Player tags must be str.
            Valid characters: 0289PYLQGRJCUV

        Returns list of Club
        """
        urls = ['{}/{}'.format(self.api.CLUB, tag) for tag in tags]
        return self._get_models(urls, model=Club)

    @typecasted
    def get_club_members(self, tag: bstag):
        """
        Get the members of a club.

        Parameters
        ----------
        tag: str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Members
        """
        url = '{}/{}/members'.format(self.api.CLUB, tag)
        return self._get_model(url, model=Members)

    @typecasted
    def get_multiple_club_members(self, tags: bstags):
        """
        Get the multiple members of a club.

        Parameters
        ----------
        tags: list of tags
            A list of valid player tags.
            Player tags must be str.
            Valid characters: 0289PYLQGRJCUV

        Returns list of Members
        """
        urls = ['{}/{}/members'.format(self.api.CLUB, tag) for tag in tags]
        return self._get_models(urls, model=Members)

    def _check_rankings(self, ranking, region, limit, brawler):
        if region is None:
            region = 'global'

        # Check for invalid parameters
        if ranking not in ('players', 'clubs', 'brawlers'):
            raise ValueError("'ranking' must be 'players', 'clubs' or 'brawlers'.")

        if not 0 < limit <= 200:
            raise ValueError('Make sure limit is between 1 and 200.')

        if ranking == 'brawlers':
            if brawler is None:
                raise ValueError('Brawler not set.')
            else:
                if isstr(brawler):
                    brawler = brawler.upper()
                elif not isinstance(brawler, int):
                    raise TypeError("`brawler` must be int or str")

                # Replace brawler name with ID
                if brawler in self.api.CURRENT_BRAWLERS.keys():
                    brawler = self.api.CURRENT_BRAWLERS[brawler]

                if brawler not in self.api.CURRENT_BRAWLERS.values():
                    raise ValueError('Invalid brawler.')

            # Construct URL
            url = '{}/{}/{}/{}?limit={}'.format(self.api.RANKINGS, region, ranking, brawler, limit)
        else:
            # Construct URL
            url = '{}/{}/{}?limit={}'.format(self.api.RANKINGS, region, ranking, limit)

        return url

    def get_rankings(self, *, ranking: str, region=None, limit: int = 200, brawler=None):
        """
        Get the top count players/clubs/brawlers.

        Parameters
        ----------
        ranking: str
            The type of ranking. Must be "players", "clubs", "brawlers".
            Anything else will return a ValueError.
        region: Optional[str]
            The region to retrieve from. Must be a 2 letter country code.
        limit: Optional[int] = 200
            The number of top players or clubs to fetch.
            If count > 200, it will return a ValueError.
        brawler: Optional[Union[str, int]] = None
            The brawler name or ID.

        Returns Ranking
        """
        url = self._check_rankings(ranking, region, limit, brawler)
        return self._get_model(url, model=Ranking)

    def get_multiple_rankings(self, *, rankings: str, regions=None, limits: int = 200, brawlers=None):
        """
        Get the multiple top count players/clubs/brawlers.

        Parameters
        ----------
        rankings: list of str
            The type of ranking. Must be "players", "clubs", "brawlers".
            Anything else will return a ValueError.
        regions: Optional[list of str]
            The region to retrieve from. Must be a 2 letter country code.
        limits: Optional[list of int] = 200
            The number of top players or clubs to fetch.
            If count > 200, it will return a ValueError.
        brawlers: Optional[list of Union[str, int]] = None
            The brawler name or ID.

        Returns Ranking
        """
        params = [rankings, regions, limits, brawlers]

        lengths = []

        for param in params:
            if isiter(param) and not isstr(param):
                lengths.append(len(param))

        if not same(lengths):
            raise ValueError("All of itersble parameters must be the same length")

        if len(lengths) < 1:
            raise ValueError("At least one argument must be iterable and not string")

        total_length = lengths[0]

        for i, data in enumerate(params):
            if not isiter(data) or isstr(data):
                params[i] = [data] * total_length

        urls = [self._check_rankings(*params) for params in zip(*params)]
        return self._get_models(urls, model=Ranking)

    def get_constants(self, key=None):
        """
        Gets Brawl Stars constants extracted from the app.

        Parameters
        ----------
        key: Optional[str] = None
            Any key to get specific data.

        Returns Constants
        """
        return self._get_model(self.api.CONSTANTS, model=Constants, key=key)

    def get_brawlers(self):
        """
        Get available brawlers and information about them.

        No parameters
        -------------

        Returns Brawlers
        """
        return self._get_model(self.api.BRAWLERS, model=Brawlers)
