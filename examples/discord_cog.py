# NOTE: This discord example is outdated as Discord's Bot API has changed

import discord
from discord.ext import commands

import brawlstats


class BrawlStars(commands.Cog, name='Brawl Stars'):
    """A simple cog for Brawl Stars commands using discord.py"""

    def __init__(self, bot):
        self.bot = bot
        self.client = brawlstats.Client('token', is_async=True)

    @commands.command()
    async def profile(self, ctx, tag: str):
        """Get a brawl stars profile"""
        try:
            player = await self.client.get_profile(tag)
        except brawlstats.RequestError as e:  # catches all exceptions
            return await ctx.send(f'```\n{e.code}: {e.message}\n```')  # sends code and error message
        em = discord.Embed(title=f'{player.name} ({player.tag})')

        em.description = f'Trophies: {player.trophies}'  # you could make this better by using embed fields
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(BrawlStars(bot))
