BrawlStats
==========

An async python wrapper for the `Brawl Stars API`_ ### Installation
Install the latest stable version by typing this into your console

::

   pip install brawlstats

Note: The wrapper and API are both still in beta If you would like to
test the *beta* version, type in

::

   pip install git+https://github.com/SharpBit/brawlstats

Documentation
~~~~~~~~~~~~~

Documentation is currently in the `docs folder`_. If you see a mistake,
open a `pull request`_ with the correct fix. ### Misc If you come across
an issue in the wrapper, please `create an issue`_ and I will look into
it ASAP. If you need help or an API Key, join the API’s `discord
server`_.

Examples
~~~~~~~~

Using an async loop.

.. code:: py

   import brawlstats
   import asyncio

   loop = asyncio.get_event_loop() # do this if you don't want to get a bunch of warnings
   client = brawlstats.Client('token', loop=loop)
   # Do not post your token on a public github

   # await only works in an async loop
   async def main():
       player = await client.get_profile('GGJVJLU2')
       print(player.trophies) # access attributes using dot notation.
       print(player.solo_showdown_victories) # access using snake_case instead of camelCase
       band = await player.get_band(full=True) # full gets the full Band object
       print(band.tag)
       best_players = band.members[0:3] # members sorted by trophies, gets best 3 players
       for player in best_players:
           print(player.name, player.trophies) # prints name and trophies
       # NOTE: this is currently not working.
       leaderboard = await client.get_leaderboard('players', 5) # gets top 5 players
       for player in leaderboard:
           print(player.name, player.position)

   # run the async loop
   loop.run_until_complete(main())

Discord Bot Cog (discord.py v1.0.0a rewrite)

.. code:: py

   import discord
   from discord.ext import commands
   import brawlstats # import the module

   class BrawlStars:
       '''A simple cog for Brawl Stars commands'''

       def __init__(self, bot):
           self.bot = bot
           self.client = brawlstats.Client('token', loop=bot.loop) # Initiliaze the client using the bot loop

       @commands.command()
       async def profile(self, ctx, tag):
           '''Get a brawl stars profile'''
           try:
               player = await self.client.get_profile(tag)
           except brawlstats.RequestError as e: # catches all exceptions
               return await ctx.send('```\n' + str(e.code) + ': ' + e.error + '\n```') # sends code and error message
           await ctx.send('Name: {0.name}\nTrophies: {0.trophies}'.format(player)) # sends player name and trophies


   def setup(bot):
       bot.add_cog(BrawlStars(bot))

.. _Brawl Stars API: http://brawlapi.cf/api
.. _docs folder: https://github.com/SharpBit/brawlstats/tree/master/docs
.. _pull request: https://github.com/SharpBit/brawlstats/pulls
.. _create an issue: https://github.com/SharpBit/brawlstats/issues
.. _discord server: https://discord.me/BrawlAPI