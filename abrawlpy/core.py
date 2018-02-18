'''
MIT License

Copyright (c) 2018 SharpBit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import aiohttp
from .utils import API
from .errors import Forbidden, InvalidTag, UnexpectedError, ServerError
from box import Box
import asyncio


class BaseBox(Box):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs, camel_killer_box=True)


class Client:
    '''
    This is an async client class that
    initializes the client

    Using this client, you can get
        - Player profile statistics
        - Band statistics
        - Current and upcoming events

    Parameters
    ------------

        token: str
            The API Key that you can get from
            https://discord.gg/r3rbf9U
        **timeout: Optional[int]
            Quits requests to the API after a number of seconds. Default=5
        **session: Optional[session]
            Use a current aiohttp session or a new one
        **loop: Optional[loop]
            Use a current loop or an new one

    Example:
    ---------

        bot.session = aiohttp.ClientSession()

        client = abrawlpy.Client(os.getenv('bstoken'), timeout=3, session=bot.session, loop=bot.loop)
        # bot is something that Discord bots have, you can use something else

    Methods
    ---------

        get_profile(tag):
            Get a brawl stars profile.
        get_band(tag):
            Get a brawl stars band.
        get_events(timeframe):
            Get current or upcoming events.

            Example
            --------
                current = client.get_events('current')
                upcoming = client.get_events('upcoming')
                both = client.get_events('both')
    '''

    def __init__(self, token, **options):
        loop = options.get('loop')
        self.session = options.get('session', aiohttp.ClientSession(loop=loop))
        self.timeout = options.get('timeout', 5)
        self.headers = {
            'Authorization': token,
            'User-Agent': 'abrawlpy | Python'
        }

    def __repr__(self):
        return f'<ABrawlPy-Client timeout={self.timeout}>'

    def __del__(self):
        self.session.close()

    def check_tag(self, tag):
        tag = tag.upper().strip("#").replace('O', '0')
        for c in tag:
            if c not in '0289PYLQGRJCUV':
                raise InvalidTag()
        return tag

    async def get_profile(self, tag):
        tag = self.check_tag(tag)
        url = f'{API.PROFILE}/{tag}'
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 403:
                    raise Forbidden(url)
                elif resp.status == 404:
                    raise InvalidTag(url)
                elif resp.status == 503:
                    raise ServerError(url)
                else:
                    raise UnexpectedError(url)
        except asyncio.TimeoutError:
            raise ServerError(url)

        return Profile(raw_data)

    get_player = get_profile

    async def get_band(self, tag):
        tag = self.check_tag(tag)
        try:
            url = f'{API.BAND}/{tag}'
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 401:
                    raise Forbidden(url)
                elif resp.status == 404:
                    raise InvalidTag(url)
                elif resp.status == 504:
                    raise ServerError(url)
                else:
                    raise UnexpectedError(url)
        except asyncio.TimeoutError:
            raise ServerError(url)

        return Band(raw_data)


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

            `full` defaults to False. This means that it will send a simple band object. If you specify it to True, then it will retrieve a full band object.
    '''

    def __repr__(self):
        return f"<Profile object name='{self.name}' tag='{self.tag}'>"

    def __str__(self):
        return f"{self.name} (#{self.tag})"

    async def get_band(self, full=False):
        if full is False:
            band = SimpleBand(self.band)
        else:
            band = Client.get_band(self.band.tag)
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
        return f"<SimpleBand object name='{self.name}' tag='{self.tag}'>"

    def __str__(self):
        return f"{self.name} (#{self.tag})"

    async def get_full(self):
        return Client.get_band(self.tag)


class Band(BaseBox):
    '''
    Returns a full band object with all
    of its attributes.
    '''

    def __repr__(self):
        return f"<Band object name='{self.name}' tag='{self.tag}'>"

    def __str__(self):
        return f"{self.name} (#{self.tag})"


class Event(BaseBox):
    '''
    Returns a current, upcoming, or both events
    '''

    def __repr__(self):
        return f"<Event object type='{self.type}'>"  # TBD
