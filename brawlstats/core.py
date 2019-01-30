import aiohttp
import asyncio
import requests
from datetime import datetime

import json
import time

from box import Box, BoxList

from .errors import MaintenanceError, NotFoundError, Unauthorized, UnexpectedError, RateLimitError, ServerError
from .utils import API


class BaseBox:
    def __init__(self, client, resp, data):
        self.client = client
        self.resp = resp
        self.from_data(data)

    def from_data(self, data):
        self.raw_data = data
        if isinstance(data, list):
            self._boxed_data = BoxList(
                data, camel_killer_box=True
            )
        else:
            self._boxed_data = Box(
                data, camel_killer_box=True
            )
        return self

    def __getattr__(self, attr):
        try:
            return getattr(self._boxed_data, attr)
        except AttributeError:
            try:
                return super().__getattr__(attr)
            except AttributeError:
                return None # makes it easier on the user's end

    def __getitem__(self, item):
        try:
            return self._boxed_data[item]
        except IndexError:
            raise IndexError('No such index: {}'.format(item))


class Client:
    """
    This is a sync/async client class that lets you access the API.

    Parameters
    ------------
    token: str
        The API Key that you can get from https://discord.me/BrawlAPI
    session: Optional[Session] = None
        Use a current session or a make new one.
    timeout: Optional[int] = 10
        A timeout for requests to the API.
    is_async: Optional[bool] = False
        Setting this to ``True`` the client async.
    url: Optional[str] = None
        Sets a different base URL to make request to. Only use this if you know what you are doing.
    loop : Optional[event loop]
        The ``event loop`` to use for asynchronous operations. Defaults to ``None``,
        in which case the default event loop is used via ``asyncio.get_event_loop()``.
        If you are passing in an aiohttp session, using this will not work. You must set it when initializing the session.
    """

    def __init__(self, token, **options):
        self.is_async = options.get('is_async', False)
        self.loop = options.get('loop', asyncio.get_event_loop())
        self.session = options.get('session') or (aiohttp.ClientSession(loop=self.loop) if self.is_async else requests.Session())
        self.timeout = options.get('timeout', 10)
        self.api = API(options.get('url'))
        self.headers = {
            'Authorization': token,
            'User-Agent': 'brawlstats | Python'
        }

    def __repr__(self):
        return '<BrawlStats-Client async={} timeout={}>'.format(self.is_async, self.timeout)

    def close(self):
        return self.session.close()

    def _check_tag(self, tag, endpoint):
        tag = tag.upper().replace('#', '').replace('O', '0')
        if len(tag) < 3:
            raise NotFoundError(endpoint + '?tag=' + tag, 404)
        for c in tag:
            if c not in '0289PYLQGRJCUV':
                raise NotFoundError(endpoint + '?tag=' + tag, 404)
        return tag

    def _raise_for_status(self, resp, text, url):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text

        code = getattr(resp, 'status', None) or getattr(resp, 'status_code')

        if 300 > code >= 200:
            return data, resp
        if code == 401:
            raise Unauthorized(url, code)
        if code in (400, 404):
            raise NotFoundError(url, code)
        if code == 429:
            raise RateLimitError(url, code, resp.headers.get('x-ratelimit-reset') - time.time())
        if code >= 500:
            if data.get('maintenance'):
                raise MaintenanceError(url, code)
            raise ServerError(url, code)

        raise UnexpectedError(url, code)

    async def _arequest(self, url):
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                return self._raise_for_status(resp, await resp.text(), url)
        except asyncio.TimeoutError:
            raise ServerError(url, 503)

    def _request(self, url):
        try:
            with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                return self._raise_for_status(resp, resp.text, url)
        except requests.Timeout:
            raise ServerError(url, 503)

    async def _aget_model(self, url, model, key=None):
        if not model:
            model = BaseBox
        data, resp = await self._arequest(url)
        if model == Constants:
            if key and not data.get(key):
                raise KeyError('No such key for Brawl Stars constants "{}"'.format(key))
            if key and data.get(key):
                return model(self, resp, data.get(key))
        return model(self, resp, data)

    def get_profile(self, tag: str):
        """Get a player's stats.

        Parameters
        ----------
        tag: str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Profile
        """
        tag = self._check_tag(tag, self.api.profile)
        url = '{}?tag={}'.format(self.api.profile, tag)
        if self.is_async:
            return self._aget_model(url, model=Profile)
        data, resp = self._request(url)

        return Profile(self, resp, data)

    get_player = get_profile

    def get_club(self, tag: str):
        """Get a club's stats.

        Parameters
        ----------
        tag: str
            A valid club tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Club
        """
        tag = self._check_tag(tag, self.api.club)
        url = '{}?tag={}'.format(self.api.club, tag)
        if self.is_async:
            return self._aget_model(url, model=Club)
        data, resp = self._request(url)

        return Club(self, resp, data)

    def get_leaderboard(self, _type: str, count: int=200):
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
        if type(count) != int:
            raise ValueError("Make sure 'count' is an int")
        if _type.lower() not in ('players', 'clubs') or not 0 < count <= 200:
            if _type.lower() not in self.api.brawlers:
                raise ValueError("Please enter 'players', 'clubs' or a brawler or make sure 'count' is between 1 and 200.")
        url = '{}/{}?count={}'.format(self.api.leaderboard, _type.lower(), count)
        if _type.lower() in self.api.brawlers:
            url = '{}/players?count={}&brawler={}'.format(self.api.leaderboard, count, _type.lower())
        if self.is_async:
            return self._aget_model(url, model=Leaderboard)
        data, resp = self._request(url)

        return Leaderboard(self, resp, data)

    def get_events(self):
        """Get current and upcoming events.

        Returns Events"""
        if self.is_async:
            return self._aget_model(self.api.events, model=Events)
        data, resp = self._request(self.api.events)

        return Events(self, resp, data)

    def get_constants(self, key=None):
        """Gets Brawl Stars constants extracted from the app.

        Parameters
        ----------
        key: Optional[str] = None
            Any key to get specific data.

        Returns Constants
        """
        if self.is_async:
            return self._aget_model(self.api.constants, model=Constants, key=key)
        data, resp = self._request(self.api.constants)
        if key and not data.get(key):
            raise KeyError('No such key for Brawl Stars constants "{}"'.format(key))
        if key and data.get(key):
            return Constants(self, resp, data.get(key))
        return Constants(self, resp, data)

    def get_misc(self):
        """Gets misc data such as shop and season info.

        Returns MiscData
        """

        if self.is_async:
            return self._aget_model(self.api.misc, model=MiscData)
        data, resp = self._request(self.api.misc)
        return MiscData(self, resp, data)

    def search_club(self, club_name: str):
        """Searches for bands of the provided club name.

        Parameters
        ----------
        club_name: str
            The query for the club search.

        Returns List\[PartialClub, ..., PartialClub\]
        """
        url = self.api.club_search + '?query=' + club_name
        if self.is_async:
            return self._aget_model(url, model=PartialClub)
        data, resp = self._request(url)
        return PartialClub(self, resp, data)

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


class Profile(BaseBox):
    """
    Returns a full player object with all of its attributes.
    """

    def __repr__(self):
        return "<Profile object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_club(self, full=True):
        """
        Gets the player's club.

        Parameters
        ----------
        full: Optional[bool] = True
            Whether or not to get the player's full club stats or not.

        Returns None, PartialClub, or Club
        """
        if not self.club:
            return None
        if not full:
            club = PartialClub(self.client, self.resp, self.club)
        else:
            club = self.client.get_club(self.club.tag)
        return club


class PartialClub(BaseBox):
    """
    Returns a simple club object with some of its attributes.
    """

    def __repr__(self):
        return "<PartialClub object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_full(self):
        """
        Gets the full club statistics.

        Returns Club
        """
        return self.client.get_club(self.tag)


class Club(BaseBox):
    """
    Returns a full club object with all of its attributes.
    """

    def __repr__(self):
        return "<Club object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)


class Leaderboard(BaseBox):
    """
    Returns a player or club leaderboard that contains a list of players or clubs.
    """

    def __len__(self):
        return sum(1 for i in self)

    def __repr__(self):
        return "<Leaderboard object count={}>".format(len(self))

    def __str__(self):
        return 'Leaderboard containing {} items'.format(len(self))

class Events(BaseBox):
    """
    Returns current and upcoming events.
    """

    def __repr__(self):
        return '<Events object>'


class Constants(BaseBox):
    """
    Returns some Brawl Stars constants.
    """

    def __repr__(self):
        return '<Constants object>'


class MiscData(BaseBox):
    """
    Misc data such as shop and season info.
    """
    pass