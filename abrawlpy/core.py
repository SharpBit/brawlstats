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
from .errors import *
from box import Box
import asyncio


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
        timeout: Optional[int]
            Quits requests to the API after a number of seconds. Default=10

    Example:
    ---------

        client = abrawlpy.Client(os.getenv('bstoken'), timeout=5)

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
        self.token = token
        self.session = aiohttp.ClientSession()
        self.timeout = options.get('timeout')  # kwargs are for more future functionality besides timeout
        self.headers = {
            'Authorization': token,
            'User-Agent': 'abrawlpy | Python'
        }

    def __repr__(self):
        return f'<ABrawlPy-Client timeout={self.timeout}>'

    def __del__(self):
        self.session.close()

    async def get_profile(self, tag):
        try:
            async with self.session.get(f'{API.PROFILE}/{tag}', timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 401:
                    raise Forbidden()
                elif resp.status == 404:
                    raise InvalidTag()
                elif resp.status == 504:
                    raise ServerError()
                else:
                    raise UnexpectedError()
        except asyncio.TimeoutError:
            raise ServerError()

        profile = Profile(raw_data, camel_killer_box=True)
        return profile

    async def get_band(self, tag):
        try:
            async with self.session.get(f'{API.BAND}/{tag}', timeout=self.timeout, headers=self.headers) as resp:
                if resp.status == 200:
                    raw_data = await resp.json()
                elif resp.status == 401:
                    raise Forbidden()
                elif resp.status == 404:
                    raise InvalidTag()
                elif resp.status == 504:
                    raise ServerError()
                else:
                    raise UnexpectedError()
        except asyncio.TimeoutError:
            raise ServerError()

        band = Band(raw_data, camel_killer_box=True)
        return band


class Profile(Box):
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
        return f"<Profile object name='{self.name}' tag={self.tag}>"

    async def get_band(self, full=False):
        if full is False:
            band = SimpleBand(self.band, camel_killer_box=True)
        else:
            band = Client.get_band(self.band.tag)
        return band


class SimpleBand(Box):
    '''
    Returns a simple band object with some of its attributes.

    Methods
    --------

        get_full():
            Gets the full band object and returns it.
    '''

    def __repr__(self):
        return f"<SimpleBand object name='{self.name}' tag='{self.tag}'>"

    async def get_full(self):
        band = Client.get_band(self.tag)
        return band


class Band(Box):
    '''
    Returns a full band object with all
    of its attributes.
    '''

    def __repr__(self):
        return f"<Band object name='{self.name}' tag='{self.tag}'>"


class Event(Box):
    '''
    Returns a current, upcoming, or both events
    '''

    def __repr__(self):
        return f"<Event object type='{self.type}'>"  # TBD
