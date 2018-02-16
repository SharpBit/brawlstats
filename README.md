# abrawlpy
An async python wrapper for the [Brawl Stars API](http://brawlstars-api.herokuapp.com/api)
### Installation
Install the latest stable version by typing this into your console
```
pip install abrawlpy
```
Note: The wrapper and API are both still in beta<br>
If you would like to test the *beta* version, type in
```
pip install git+https://github.com/SharpBit/abrawlpy
```
### Documentation
Documentation is coming soon! If you would like to help, DM SharpBit#9614 on Discord or open a [pull request](https://github.com/SharpBit/abrawlpy/pulls)
### Misc
If you come across an issue in the wrapper, please [create an issue](https://github.com/SharpBit/abrawl-py) and I will look into it ASAP.

### Examples

Using an async loop
```py
import abrawlpy
import asyncio

client = abrawlpy.Client('token', timeout=5)
# Do not post your token on a public github


async def main():
    player = await client.get_profile('UG99J2')
    print(player.trophies) # access attributes using dot notation.
    print(player.showdown_victories) # access using snake_case instead of camelCase
    band = await player.get_band()
    print(band.tag)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
Discord Bot Cog (Python 3.6 discord.py v1.0.0a (rewrite)
```py
import discord
from discord.ext import commands
import abrawlpy

class BrawlStars:
    '''A simple cog for Brawl Stars commands'''

    def __init__(self, bot):
        self.bot = bot
        self.client = abrawlpy.Client('token', timeout=5)

    @commands.command()
    async def profile(self, ctx, tag):
        '''Get a brawl stars profile'''
        player = await self.client.get_profile(tag)
        await ctx.send(player.name)
        await ctx.send(player.trophies)


def setup(bot):
    bot.add_cog(BrawlStars(bot))
```
