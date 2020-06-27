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
            # sends code and error message
            return await ctx.send('```\n{}: {}\n```'.format(e.code, e.message))
        em = discord.Embed(title='{0.name} ({0.tag})'.format(player))

        # you could make this better by using embed fields
        em.description = 'Trophies: {}'.format(player.trophies)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(BrawlStars(bot))
