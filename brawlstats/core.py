import aiohttp
import asyncio

from box import Box
from json import JSONDecodeError

from .errors import InvalidTag, Unauthorized, UnexpectedError, ServerError
from .utils import API


class BaseBox(Box):
    def __init__(self, *args, **kwargs):
        kwargs['camel_killer_box'] = True
        super().__init__(*args, **kwargs)


class Client:
    '''
    This is an async client class that
    initializes the client

    Using this client, you can get
        - Player profile statistics
        - Band statistics
        - Player and band leaderboards

    Parameters
    ------------

        token: str
            The API Key that you can get from
            https://discord.me/BrawlAPI
        **timeout: Optional[int]
            Quits requests to the API after a number of seconds. Default=5
        **session: Optional[session]
            Use a current aiohttp session or a new one
        **loop: Optional[loop]
            Use a current loop. Recommended to remove warnings when you run the program.

    Example:
    ---------

        bot.session = aiohttp.ClientSession()

        # get your token by joining our API server and typing .getToken at https://discord.me/BrawlAPI
        client = brawlstats.Client(os.getenv('bstoken'), session=bot.session, loop=bot.loop)
        # bot is something that Discord bots have, you can use something else

    Methods
    ---------

        get_profile(tag):
            Get a brawl stars profile.
        get_band(tag):
            Get a brawl stars band.
        get_leaderboard(p_or_b, count):
            Get a player or band leaderboard with count players/bands.

            Examples
            --------
                profile = await client.get_profile('GGJVJLU2')
                p_lb = await client.get_leaderboard('players', 5)
                # gets top five players
    '''

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

    def __del__(self):
        self.session.loop.run_until_complete(self.session.close())

    def check_tag(self, tag, endpoint):
        tag = tag.upper().replace('#', '').replace('O', '0')
        for c in tag:
            if c not in '0289PYLQGRJCUV':
                raise InvalidTag(endpoint + '/' + tag)
        return tag

    async def _aget(self, url):
        '''Gets the response from the API.'''
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 403:
                    raise Unauthorized(url)
                elif resp.status == 404:
                    raise InvalidTag(url)
                elif resp.status == 503:
                    raise ServerError(url)
                else:
                    raise UnexpectedError(url)
        except (asyncio.TimeoutError, JSONDecodeError):
            raise ServerError(url)
        return raw_data

    async def get_profile(self, tag):
        tag = self.check_tag(tag, API.PROFILE)
        response = await self._aget(API.PROFILE + '/' + tag)
        response['client'] = self

        return Profile(response)

    get_player = get_profile

    async def get_band(self, tag):
        tag = self.check_tag(tag, API.BAND)
        response = await self._aget(API.BAND + '/' + tag)

        return Band(response)

    async def get_leaderboard(self, p_or_b, count=200):
        if p_or_b not in ('players', 'bands') or count > 200:
            raise ValueError("Please enter 'players' or 'bands' or make sure 'count' is 200 or less.")
        url = API.LEADERBOARD + '/' + p_or_b + '/' + str(count)
        response = await self._aget(url)

        if p_or_b == 'players':
            return Leaderboard(response['players'])
        else:
            return Leaderboard(response['bands'])


class Profile(BaseBox):
    '''
    Returns a full player object with all
    of its attributes.

    Methods
    --------
        get_band(full=False):
            Returns a Band object for the player's band.
            If the player is not in a band,
            it returns None

            `full` defaults to False. This means that it will send a simple band object.
            If you specify it to True, then it will retrieve a full band object.
    '''

    def __repr__(self):
        return "<Profile object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    async def get_band(self, full=False):
        if not full:
            self.band['client'] = self.client
            band = SimpleBand(self.band)
        else:
            band = await self.client.get_band(self.band.tag)
        return band


class SimpleBand(BaseBox):
    '''
    Returns a simple band object with some of its attributes.

    Methods
    --------

        get_full():
            Gets the full band object and returns it.
    '''

    def __repr__(self):
        return "<SimpleBand object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)

    async def get_full(self):
        return await self.client.get_band(self.tag)


class Band(BaseBox):
    '''
    Returns a full band object with all
    of its attributes.
    '''

    def __repr__(self):
        return "<Band object name='{0.name}' tag='{0.tag}'>".format(self)

    def __str__(self):
        return '{0.name} (#{0.tag})'.format(self)


class Leaderboard(BaseBox):
    '''
    Returns a player or band leaderboard
    that contains a list of players or bands.
    '''

    def __repr__(self):
        return '<Leaderboard object count={}'.format(len(self))

    def __str__(self):
        return '{} Leaderboard containing {} items'.format(len(self))
