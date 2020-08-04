import asyncio
import json
import logging
import sys
import time

import aiohttp
import requests
from cachetools import TTLCache

from .errors import IncorrectDataError, Forbidden, NotFoundError, RateLimitError, ServerError, UnexpectedError
from .models import BattleLog, Brawlers, Club, Constants, Members, Player, Ranking
from .utils import API, bstag, bstags, isiter, not_unique, typecasted, same

log = logging.getLogger(__name__)


from asyncio_throttle import Throttler


class ThrottledClientSession(aiohttp.ClientSession):
    """Rate-throttled client session class inherited from aiohttp.ClientSession)"""
    def __init__(self, *args, rate_limit=1, sleep_time=None, min_sleep=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate_limit = rate_limit
        self._fillerTask = None
        self._queue = None
        self.min_sleep = min_sleep

        if rate_limit < 1:
            raise ValueError('`rate_limit` must be positive')

        # (increment, sleep) = self._get_rate_increment()
        size = 2  # min(1, int(rate_limit)) + 1
        self._queue = asyncio.Queue(size)

        if sleep_time is None:
            self.sleep_time = max(1 / self.rate_limit, self.min_sleep)
        else:
            self.sleep_time = sleep_time

        self._fillerTask = asyncio.create_task(self._filler())
        # self._start_time = None
        # self._count = 0

    async def close(self):
        """
        Close rate-limiter's "bucket filler" task
        """
        # DEBUG 
        if self._start_time is not None:
            duration = time.time() - self._start_time
            # print('Average WG API request rate: ' + #'{:.1f}'.format(self._count / duration) + ' / sec')
        if self._fillerTask is not None:
            self._fillerTask.cancel()
        try:
            await asyncio.wait_for(self._fillerTask, timeout=3)
        except asyncio.TimeoutError as err:
            print(str(err))
        await super().close()

    async def _filler(self):
        """
        Filler task to fill the leaky bucket algo
        """
        try:
            if self._queue is None:
                return None
            # print('SLEEP: ' + str(sleep))
            updated_at = time.monotonic()
            fraction = 0
            extra_increment = 0

            for i in range(self._queue.maxsize):
                self._queue.put_nowait(i)

            while True:
                if not self._queue.full():
                    now = time.monotonic()
                    increment = self.rate_limit * (now - updated_at)
                    fraction += increment % 1
                    extra_increment = fraction // 1
                    items_2_add = int(min(self._queue.maxsize - self._queue.qsize(), int(increment) + extra_increment))
                    fraction = fraction % 1
                    for i in range(0, items_2_add):
                        self._queue.put_nowait(i)
                    updated_at = now
                await asyncio.sleep(self.sleep_time)
        except asyncio.CancelledError:
            raise Exception("Cancelled")
            # debug('Cancelled')
        except Exception as err:
            raise err
            # error(exception=err)

    async def _allow(self):
        if self._queue is not None:
            # debug 
            #if self._start_time == None:
            #    self._start_time = time.time()
            await self._queue.get()
            self._queue.task_done()
            # DEBUG 
            #self._count += 1

    async def _request(self, *args, **kwargs):
        """
        Throttled _request()
        """
        await self._allow()
        return await super()._request(*args, **kwargs)


#@staticmethod
def _timeout(func):
    # @staticmethod
    async def wrapper(url):
        try:
            return await func(url)
        except asyncio.TimeoutError:
            raise ServerError(503, url)
    return wrapper


#@staticmethod
# def _settings(use_lock=False, use_wait=False, waiting_time=0, lock=None):
#     def decorator(func):
#         if use_wait:
#             async def wrapper2(url):
#                 data = await func(url)
#                 await asyncio.sleep(waiting_time)
#                 return data

#             func = wrapper2

#         if use_lock:
#             async def wrapper1(url):
#                 # Use lock if prevent_ratelimit=True
#                 async with lock:
#                     return await func(url)

#             func = wrapper1

#         return func
#     return decorator


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
    prevent_ratelimit: Optional[bool] = False
        Whether or not to wait between requests to prevent being ratelimited.
    base_url: Optional[str] = None
        Sets a different base URL to make request to.
    waiting_time: Optional[float] = 0.01
        Timeout between requests, works if prevent_ratelimit = True
    """

    REQUEST_LOG = '{method} {url} recieved {text} has returned {status}'

    def __init__(self, token, session=None, timeout=30, is_async=False, **options):
        # Async options
        self.is_async = is_async
        self.loop = options.get('loop', asyncio.get_event_loop()) if self.is_async else None
        self.connector = options.get('connector')

        self.debug = options.get('debug', False)
        self.cache = TTLCache(3200 * 3, 60 * 3)  # 3200 requests per minute

        self.use_models = options.get('use_models')

        faster_type = options.get('faster_type')

        rate_limit = options.get('rate_limit', 1)

        if faster_type != 1:
            # Session and request options
            session = aiohttp.ClientSession(
                loop=self.loop,
                connector=self.connector,
            )

        #limiter = asyncio.Lock(loop=self.loop)
        limiter = None

        if faster_type[0]:
            # Session and request options
            session = ThrottledClientSession(
                loop=self.loop,
                connector=self.connector,
                rate_limit=rate_limit,
            )
        if faster_type[1]:
            limiter = Throttler(rate_limit=rate_limit)  # 3200, period=60)  # 80
        if faster_type[2]:
            limiter = self.lock = asyncio.Semaphore(rate_limit, loop=self.loop)

        self.session = options.get('session') or (
            session if self.is_async else requests.Session()
        )

        self.req = options.get('req')

        self.timeout = timeout
        self.prevent_ratelimit = options.get('prevent_ratelimit', False)
        self.waiting_time = options.get('waiting_time', 0.1)
        if self.is_async and self.prevent_ratelimit:
            self.lock = limiter
        self.api = API(base_url=options.get('base_url'), version=1)
        self.use_lock = options.get('use_lock') or sys.version_info < (3, 8)
        self.use_wait = options.get('use_wait', False)

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

    async def _fetch(self, url):
        # try:
        #     async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
        #         return resp, await resp.text()
        # except asyncio.TimeoutError:
        #     raise ServerError(503, url)
        async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
            return resp, await resp.text(), await resp.json()

    async def _arequest_wait(self, url):
        data = await self._fetch(url)
        await asyncio.sleep(self.waiting_time)
        return data

    async def _arequest_no_wait(self, url):
        return await self._fetch(url)

    async def _arequest_lock_wait(self, url):
        # Use self.lock if prevent_ratelimit=True
        async with self.lock:
            return await self._arequest_wait(url)

    async def _arequest_lock_no_wait(self, url):
        # Use self.lock if prevent_ratelimit=True
        async with self.lock:
            return await self._arequest_no_wait(url)

    async def _arequest_no_lock_wait(self, url):
        return await self._arequest_wait(url)

    async def _arequest_no_lock_no_wait(self, url):
        return await self._arequest_no_wait(url)

    async def _arequests2(self, urls):
        """Async method to request a urls."""
        tasks = {}
        from_cache = {}

        if self.prevent_ratelimit:
            if self.use_lock:
                if self.use_wait:
                    func = self._arequest_lock_wait
                else:
                    func = self._arequest_lock_no_wait
            else:
                if self.use_wait:
                    func = self._arequest_no_lock_wait
                else:
                    func = self._arequest_no_lock_no_wait
        else:
            func = self._fetch

        func = _timeout(func)

        for url in urls:
            # Try and retrieve from cache
            cache = self._resolve_cache(url)
            if cache is not None:
                from_cache[url] = cache
                continue

            tasks[url] = asyncio.ensure_future(func(url))

        self.tasks = tasks

        start = time.time()

        await asyncio.gather(*tasks.values())#, loop=self.loop)#, return_exceptions=True)

        self.time_ = time.time() - start

        for url, task in tasks.items():
            # Cache the data if successful
            self.cache[url] = from_cache[url] = self._raise_for_status(*task._result)

        return [from_cache[url] for url in urls]

    async def _arequests(self, urls):
        tasks = []

        for url in urls:
            task = asyncio.ensure_future(self._arequest_ratelimit(url))  # _arequest
            tasks.append(task)

        self.tasks = tasks

        return await asyncio.gather(*tasks)

    async def _arequest_ratelimit(self, url):
        if self.prevent_ratelimit:
            # Use self.lock if prevent_ratelimit=True
            if self.use_lock:
                async with self.lock:
                    data = await self._arequest(url)
                    if self.use_wait:
                        await asyncio.sleep(self.waiting_time)
            else:
                data = await self._arequest(url)
                if self.use_wait:
                    await asyncio.sleep(self.waiting_time)
        else:
            data = await self._arequest(url)
        
        return data

    async def _arequest(self, url):
        """Async method to request a url."""
        # Try and retrieve from cache
        cache = self._resolve_cache(url)
        if cache is not None:
            return cache

        try:
            req = self.session.get(
                url, timeout=self.timeout, headers=self.headers,
            )
            async with req as resp:
                data = self._raise_for_status(resp, await resp.text(), await resp.json())
        except asyncio.TimeoutError:
            raise ServerError(503, url)
        else:
            # Cache the data if successful
            self.cache[url] = data

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

    async def _aget_model(self, url, model, key=None):
        """Method to turn the response data into a Model class for the async client."""
        if self.prevent_ratelimit:
            # Use self.lock if prevent_ratelimit=True
            if self.use_lock:
                async with self.lock:
                    data = await self._arequest(url)
                    if self.use_wait:
                        await asyncio.sleep(self.waiting_time)
            else:
                data = await self._arequest(url)
                if self.use_wait:
                    await asyncio.sleep(self.waiting_time)
        else:
            data = await self._arequest(url)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError('No such Constants key "{}"'.format(key))

        return model(self, data)

    def _get_model(self, url, model, key=None):
        """Method to turn the response data into a Model class for the sync client."""
        if self.is_async:
            # Calls the async function
            return self._aget_model(url, model=model, key=key)

        data = self._request(url)
        if self.prevent_ratelimit:
            time.sleep(self.waiting_time)

        if model == Constants:
            if key:
                if data.get(key):
                    return model(self, data.get(key))
                else:
                    raise KeyError('No such Constants key "{}"'.format(key))

        return model(self, data)

    async def _aget_models(self, urls, model):
        start = time.time()

        if self.req == 1:
            res = await self._arequests(urls)
        elif self.req == 2:
            res = await self._arequests2(urls)

        self.time_1 = time.time() - start

        start = time.time()

        if self.use_models:
            return_data = [model(self, data) for data in res]
        else:
            return_data = res

        self.time_2 = time.time() - start

        return return_data

    def _get_models(self, urls, model):
        # check the uniqueness of all urls
        if len(urls) > 1 and not_unique(urls):
            raise ValueError("not all arguments in iterable are unique")

        if self.is_async:
            # Calls the async function
            return self._aget_models(urls, model=model)

        data = self._grequests(urls)

        for url in urls:
            data = self._request(url)
            if self.prevent_ratelimit:
                time.sleep(self.waiting_time)

        return model(self, data)

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
                if isinstance(brawler, str):
                    brawler = brawler.lower()

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

    def get_rankings(self, *, ranking: str, region=None, limit: int=200, brawler=None):
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

    def get_multiple_rankings(self, *, rankings: str, regions=None, limits: int=200, brawlers=None):
        params = [rankings, regions, limits, brawlers]

        lengths = []

        for param in params:
            if isiter(param):
                lengths.append(len(param))

        if not same(lengths):
            raise ValueError("all of itersble parameters must be the same length")

        len_ = lengths[0]

        for i in range(len(params)):
            if not isiter(params[i]):
                params[i] = [params[i] for _ in range(len_)]

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

        Returns Brawlers
        """
        return self._get_model(self.api.BRAWLERS, model=Brawlers)
