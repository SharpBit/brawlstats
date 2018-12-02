import aiohttp
import asyncio
import requests

import json

from box import Box, BoxList

from .errors import NotFoundError, Unauthorized, UnexpectedError, ServerError
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
            return getattr(self._boxed_data, item)
        except AttributeError:
            raise KeyError('No such key: {}'.format(item))


class Client:
    """
    This is a sync/async client class that lets you access the API.

    Parameters
    ------------
    token: str
        The API Key that you can get from https://discord.me/BrawlAPI
    timeout: Optional[int] = 10
        A timeout for requests to the API.
    session: Optional[Session] = None
        Use a current session or a make new one.
    is_async: Optional[bool] = False
        Setting this to ``True`` the client async.
    url: Optional[str] = None
        Sets a different base URL to make request to. Only use this if you know what you are doing.
    """

    def __init__(self, token, **options):
        self.is_async = options.get('is_async', False)
        self.session = options.get('session', aiohttp.ClientSession() if self.is_async else requests.Session())
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
            raise NotFoundError(endpoint + '/' + tag, 404)
        for c in tag:
            if c not in '0289PYLQGRJCUV':
                raise NotFoundError(endpoint + '/' + tag, 404)
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
        if code >= 500:
            raise ServerError(url, code)

        raise UnexpectedError(url, code)

    async def _aget(self, url):
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                return self._raise_for_status(resp, await resp.text(), url)
        except asyncio.TimeoutError:
            raise ServerError(url, 503)

    def _get(self, url):
        try:
            with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                return self._raise_for_status(resp, resp.text, url)
        except requests.Timeout:
            raise ServerError(url, 503)

    async def _get_profile_async(self, tag: str):
        data, resp = await self._aget(self.api.profile + '/' + tag)
        return Profile(self, resp, data)

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
        if self.is_async:
            return self._get_profile_async(tag)
        data, resp = self._get(self.api.profile + '/' + tag)

        return Profile(self, resp, data)

    get_player = get_profile

    async def _get_band_async(self, tag: str):
        data, resp = await self._aget(self.api.band + '/' + tag)
        return Band(self, resp, data)

    def get_band(self, tag: str):
        """Get a band's stats.

        Parameters
        ----------
        tag: str
            A valid band tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Band
        """
        tag = self._check_tag(tag, self.api.band)
        if self.is_async:
            return self._get_band_async(tag)
        data, resp = self._get(self.api.band + '/' + tag)

        return Band(self, resp, data)

    async def _get_leaderboard_async(self, url):
        data, resp = await self._aget(url)
        return Leaderboard(self, resp, data)

    def get_leaderboard(self, player_or_band: str, count: int=200):
        """Get the top count players/bands.

        Parameters
        ----------
        player_or_band: str
            The string must be 'players' or 'bands'.
            Anything else will return a ValueError.
        count: Optional[int] = 200
            The number of top players or bands to fetch.
            If count > 200, it will return a ValueError.

        Returns Leaderboard
        """
        if type(count) != int:
            raise ValueError("Make sure 'count' is an int")
        if player_or_band.lower() not in ('players', 'bands') or count > 200 or count < 1:
            raise ValueError("Please enter 'players' or 'bands' or make sure 'count' is between 1 and 200.")
        url = self.api.leaderboard + '/' + player_or_band + '/' + str(count)
        if self.is_async:
            return self._get_leaderboard_async(url)
        data, resp = self._get(url)

        return Leaderboard(self, resp, data)

    async def _get_events_async(self):
        data, resp = await self._aget(self.api.events)
        return Events(self, resp, data)

    def get_events(self):
        """Get current and upcoming events.

        Returns Events"""
        if self.is_async:
            return self._get_events_async()
        data, resp = self._get(self.api.events)

        return Events(self, resp, data)

class Profile(BaseBox):
    """
    Returns a full player object with all of its attributes.
    """

    def __repr__(self):
        return "<Profile object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_band(self, full=False):
        """
        Gets the player's band.

        Parameters
        ----------
        full: Optional[bool] = False
            Whether or not to get the player's full band stats or not.

        Returns None, SimpleBand, or Band
        """
        if not self.band:
            return None
        if not full:
            band = SimpleBand(self.client, self.resp, self.band)
        else:
            band = self.client.get_band(self.band.tag)
        return band


class SimpleBand(BaseBox):
    """
    Returns a simple band object with some of its attributes.
    """

    def __repr__(self):
        return "<SimpleBand object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    def get_full(self):
        """
        Gets the full band statistics.

        Returns Band
        """
        return self.client.get_band(self.tag)


class Band(BaseBox):
    """
    Returns a full band object with all of its attributes.
    """

    def __repr__(self):
        return "<Band object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)


class Leaderboard(BaseBox):
    """
    Returns a player or band leaderboard that contains a list of players or bands.
    """

    def __repr__(self):
        lb_type = 'player' if self.players else 'band'
        count = len(self.players) if self.players else len(self.bands)
        return "<Leaderboard object type='{}' count={}>".format(lb_type, count)

    def __str__(self):
        lb_type = 'Player' if self.players else 'Band'
        count = len(self.players) if self.players else len(self.bands)
        return '{} Leaderboard containing {} items'.format(lb_type, count)

class Events(BaseBox):
    """
    Returns current and upcoming events.
    """

    def __repr__(self):
        return '<Events object>'

    def __str__(self):
        return 'Events object'
