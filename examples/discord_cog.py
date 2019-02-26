import discord
from discord.ext import commands
import brawlstats

class BrawlStars:
    """A simple cog for Brawl Stars commands using discord.py rewrite (v1.0.0a)"""

    def __init__(self, bot):
        self.bot = bot
        self.client = brawlstats.Client('token', is_async=True)

    @commands.command()
    async def profile(self, ctx, tag: str):
        """Get a brawl stars profile"""
        try:
            player = await self.client.get_profile(tag)
        except brawlstats.RequestError as e:  # catches all exceptions
            return await ctx.send('```\n{}: {}\n```'.format(e.code, e.error))  # sends code and error message
        em = discord.Embed(title='{0.name} ({0.tag})'.format(player))
        em.description = 'Trophies: {}'.format(player.trophies)  # you could make this better by using embed fields
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(BrawlStars(bot))
