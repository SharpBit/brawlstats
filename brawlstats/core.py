import aiohttp
import asyncio
import logging
import requests
from cachetools import TTLCache
from datetime import datetime

import json
import sys
import time

from .errors import MaintenanceError, NotFoundError, Unauthorized, UnexpectedError, RateLimitError, ServerError
from .models import Club, Constants, Events, Leaderboard, MiscData, PartialClub, Profile
from .utils import API, bstag

log = logging.getLogger(__name__)


class Client:
    """
    This is a sync/async client class that lets you access the API.

    Parameters
    ------------
    token: str
        The API Key that you can get from https://discord.me/BrawlAPI
    session: Optional[Session] = None
        Use a current session or a make new one. Can be ``aiohttp.ClientSession()`` or ``requests.Session()``
    timeout: Optional[int] = 10
        A timeout in seconds for requests to the API.
    is_async: Optional[bool] = False
        Setting this to ``True`` makes the client async.
    loop: Optional[event loop]
        The ``event loop`` to use for asynchronous operations. Defaults to ``None``,
        in which case the default event loop is used via ``asyncio.get_event_loop()``.
        If you are passing in an aiohttp session, using this will not work. You must set it when initializing the session.
    debug: Optional[bool] = False
        Whether or not to give you more info to debug easily.
    base_url: Optional[str] = None
        Sets a different base URL to make request to. Only use this if you know what you are doing.
    """

    REQUEST_LOG = '{method} {url} recieved {text} and returned status code {status}'

    def __init__(self, token, **options):
        self.is_async = options.get('is_async', False)
        self.loop = options.get('loop', asyncio.get_event_loop())
        self.session = options.get('session') or (aiohttp.ClientSession(loop=self.loop) if self.is_async else requests.Session())
        self.timeout = options.get('timeout', 10)
        self.api = API(options.get('base_url'))
        self.debug = options.get('debug', False)
        self.cache = TTLCache(900, 180)  # 5 requests/sec
        self.headers = {
            'Authorization': token,
            'User-Agent': 'brawlstats/{} (Python {})'.format(self.api.VERSION, sys.version[:3])
        }

    def __repr__(self):
        return '<BrawlStats-Client async={} timeout={}>'.format(self.is_async, self.timeout)

    def close(self):
        return self.session.close()

    def _raise_for_status(self, resp, text, url):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text

        code = getattr(resp, 'status', None) or getattr(resp, 'status_code')

        if self.debug:
            log.debug(self.REQUEST_LOG.format(method='GET', url=resp.url, text=text, status=code))

        if 300 > code >= 200:
            return (data, resp)
        if code == 401:
            raise Unauthorized(url, code)
        if code in (400, 404):
            raise NotFoundError(url, code)
        if code == 429:
            raise RateLimitError(url, code, resp.headers.get('x-ratelimit-reset') - time.time())
        if code >= 500:
            if isinstance(data, str):  # Cloudflare error
                raise ServerError(url, code)
            if data.get('maintenance'):
                raise MaintenanceError(url, code)
            raise ServerError(url, code)

        raise UnexpectedError(url, code, data)

    def _resolve_cache(self, url):
        data = self.cache.get(url)
        if not data:
            return None
        resp = 'Cached Data'
        if self.debug:
            log.debug('GET {} got result from cache.'.format(url))
        return (data, resp)

    async def _arequest(self, url):
        data = self._resolve_cache(url)
        if not data:
            try:
                async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                    data = self._raise_for_status(resp, await resp.text(), url)
            except asyncio.TimeoutError:
                raise ServerError(url, 503)
            else:
                self.cache[url] = data[0]

        return data

    def _request(self, url):
        data = self._resolve_cache(url)
        if not data:
            try:
                with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                    data = self._raise_for_status(resp, resp.text, url)
            except requests.Timeout:
                raise ServerError(url, 503)
            else:
                self.cache[url] = data[0]

        return data

    async def _aget_model(self, url, model, key=None):
        data, resp = await self._arequest(url)
        if model == Constants:
            if key and not data.get(key):
                raise KeyError('No such key for Brawl Stars constants "{}"'.format(key))
            if key and data.get(key):
                return model(self, resp, data.get(key))
        if model == PartialClub and isinstance(data, list):
            return [model(self, resp, data) for club in data]
        return model(self, resp, data)

    def _get_model(self, url, model, key=None):
        if self.is_async:
            return self._aget_model(url, model=model, key=key)
        data, resp = self._request(url)
        if model == Constants:
            if key and not data.get(key):
                raise KeyError('No such key for Brawl Stars constants "{}"'.format(key))
            if key and data.get(key):
                return model(self, resp, data.get(key))
        if model == PartialClub and isinstance(data, list):
            return [model(self, resp, data) for club in data]
        return model(self, resp, data)

    def get_profile(self, tag: bstag):
        """Get a player's stats.

        Parameters
        ----------
        tag: str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Profile
        """
        url = '{}?tag={}'.format(self.api.PROFILE, tag)

        return self._get_model(url, model=Profile)

    get_player = get_profile

    def get_club(self, tag: bstag):
        """Get a club's stats.

        Parameters
        ----------
        tag: str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Club
        """
        url = '{}?tag={}'.format(self.api.CLUB, tag)

        return self._get_model(url, model=Club)

    def get_leaderboard(self, lb_type: str, count: int=200):
        """Get the top count players/clubs/brawlers.

        Parameters
        ----------
        type: str
            The type of leaderboard. Must be "players", "clubs", or the brawler leaderboard you are trying to access.
            Anything else will return a ValueError.
        count: Optional[int] = 200
            The number of top players or clubs to fetch.
            If count > 200, it will return a ValueError.

        Returns Leaderboard
        """
        lb_type = lb_type.lower()
        if type(count) != int:
            raise ValueError("Make sure 'count' is an int")
        if lb_type not in self.api.BRAWLERS + ['players', 'clubs'] or not 0 < count <= 200:
            raise ValueError("Please enter 'players', 'clubs' or a brawler or make sure 'count' is between 1 and 200.")
        url = '{}/{}?count={}'.format(self.api.LEADERBOARD, lb_type, count)
        if lb_type in self.api.BRAWLERS:
            url = '{}/players?count={}&brawler={}'.format(self.api.LEADERBOARD, count, lb_type)

        return self._get_model(url, model=Leaderboard)

    def get_events(self):
        """Get current and upcoming events.

        Returns Events"""
        return self._get_model(self.api.EVENTS, model=Events)

    def get_constants(self, key=None):
        """Gets Brawl Stars constants extracted from the app.

        Parameters
        ----------
        key: Optional[str] = None
            Any key to get specific data.

        Returns Constants
        """
        return self._get_model(self.api.CONSTANTS, model=Constants, key=key)

    def get_misc(self):
        """Gets misc data such as shop and season info.

        Returns MiscData
        """

        return self._get_model(self.api.MISC, model=MiscData)

    def search_club(self, club_name: str):
        """Searches for bands of the provided club name.

        Parameters
        ----------
        club_name: str
            The query for the club search.

        Returns List\[PartialClub, ..., PartialClub\]
        """
        url = self.api.CLUB_SEARCH + '?name=' + club_name
        return self._get_model(url, model=PartialClub)

    def get_datetime(self, timestamp: str, unix=True):
        """Converts a %Y%m%dT%H%M%S.%fZ to a UNIX timestamp
        or a datetime.datetime object
        Parameters
        ---------
        timestamp: str
            A timestamp in the %Y-%m-%dT%H:%M:%S.%fZ format, usually returned by the API
            in the ``created_time`` field for example (eg. 2018-07-18T14:59:06.000Z)
        unix: Optional[bool] = True
            Whether to return a POSIX timestamp (seconds since epoch) or not
        Returns int or datetime.datetime
        """
        time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        if unix:
            return int(time.timestamp())
        else:
            return time
