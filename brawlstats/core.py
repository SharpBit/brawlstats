import aiohttp
import asyncio

from box import Box

from .errors import BadRequest, InvalidTag, NotFoundError, Unauthorized, UnexpectedError, ServerError
from .utils import API


class BaseBox(Box):
    def __init__(self, *args, **kwargs):
        kwargs['camel_killer_box'] = True
        super().__init__(*args, **kwargs)


class Client:
    """
    This is an async client class that lets you access the API.

    Parameters
    ------------
    token: str
        The API Key that you can get from https://discord.me/BrawlAPI
    timeout: Optional[int] = 5
        A timeout for requests to the API.
    session: Optional[Session] = aiohttp.ClientSession()
        Use a current aiohttp session or a new one.
    loop: Optional[Loop] = None
        Use a current loop. Recommended to remove warnings when you run the program.
    """

    def __init__(self, token, **options):
        loop = options.get('loop', asyncio.get_event_loop())
        self.session = options.get('session', aiohttp.ClientSession(loop=loop))
        self.timeout = options.get('timeout', 5)
        self.headers = {
            'Authorization': token,
            'User-Agent': 'brawlstats | Python'
        }

    def __repr__(self):
        return '<BrawlStats-Client timeout={}>'.format(self.timeout)

    async def close(self):
        return await self.session.close()

    def _check_tag(self, tag, endpoint):
        tag = tag.upper().replace('#', '').replace('O', '0')
        if len(tag) < 3:
            raise InvalidTag(endpoint + '/' + tag, 404)
        for c in tag:
            if c not in '0289PYLQGRJCUV':
                raise InvalidTag(endpoint + '/' + tag, 404)
        return tag

    async def _aget(self, url):
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 400:
                    raise BadRequest(url, resp.status)
                elif resp.status == 403:
                    raise Unauthorized(url, resp.status)
                elif resp.status == 404:
                    raise InvalidTag(url, resp.status)
                elif resp.status in (503, 520, 521):
                    raise ServerError(url, resp.status)
                else:
                    raise UnexpectedError(url, resp.status)
        except asyncio.TimeoutError:
            raise NotFoundErrorurl, 400)
        return raw_data

    async def get_profile(self, tag: str):
        """Get a player's stats.

        Parameters
        ----------
        tag: str
            A valid player tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Profile
        """
        tag = self._check_tag(tag, API.PROFILE)
        response = await self._aget(API.PROFILE + '/' + tag)
        response['client'] = self

        return Profile(response)

    get_player = get_profile

    async def get_band(self, tag: str):
        """Get a band's stats.

        Parameters
        ----------
        tag: str
            A valid band tag.
            Valid characters: 0289PYLQGRJCUV

        Returns Band
        """
        tag = self._check_tag(tag, API.BAND)
        response = await self._aget(API.BAND + '/' + tag)

        return Band(response)

    async def get_leaderboard(self, player_or_band: str, count: int=200):
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
        url = API.LEADERBOARD + '/' + player_or_band + '/' + str(count)
        response = await self._aget(url)

        return Leaderboard(response)


class Profile(BaseBox):
    """
    Returns a full player object with all of its attributes.
    """

    def __repr__(self):
        return "<Profile object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    async def get_band(self, full=False):
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
            self.band['client'] = self.client
            band = SimpleBand(self.band)
        else:
            band = await self.client.get_band(self.band.tag)
        return band


class SimpleBand(BaseBox):
    """
    Returns a simple band object with some of its attributes.
    """

    def __repr__(self):
        return "<SimpleBand object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    async def get_full(self):
        """
        Gets the full band statistics.

        Returns Band
        """
        return await self.client.get_band(self.tag)


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
        return '<Leaderboard object count={}'.format(len(self))

    def __str__(self):
        return '{} Leaderboard containing {} items'.format(len(self))
