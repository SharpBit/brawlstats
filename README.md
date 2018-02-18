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
Documentation is currently in the [docs folder](https://github.com/SharpBit/abrawlpy/tree/master/docs). If you see a mistake, open a [pull request](https://github.com/SharpBit/abrawlpy/pulls) with the correct fix.
### Misc
If you come across an issue in the wrapper, please [create an issue](https://github.com/SharpBit/abrawlpy/issues) and I will look into it ASAP.

### Examples

Using an async loop.
```py
import abrawlpy
import asyncio

client = abrawlpy.Client('token', timeout=5)
# Do not post your token on a public github

# await only works in an async loop
async def main():
    player = await client.get_profile('UG99J2')
    print(player.trophies) # access attributes using dot notation.
    print(player.showdown_victories) # access using snake_case instead of camelCase
    band = await player.get_band()
    print(band.tag)
    best_players = band.members[0:3] # members sorted by trophies, gets best 3 players
    for player in best_players:
        print(player.name, player.trophies) # prints name and trophies

# run the async loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
Discord Bot Cog (Python 3.6 discord.py v1.0.0a rewrite)
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
        try:
            player = await self.client.get_profile(tag)
        except abrawlpy.errors.RequestError as e:
            return await ctx.send(f'```\n{e.code}: {e.error}\n```')
        await ctx.send(f'Name: {player.name}')
        await ctx.send(f'Trophies: {player.trophies}')


def setup(bot):
    bot.add_cog(BrawlStars(bot))
```
