from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def _purge(self, ctx: commands.Context, amount: int = 5) -> None:
        await ctx.channel.purge(limit=amount + 1)

        await self.utils.command_result(
            ctx,
            result=LucidCommandResult.SUCCESS,
        )


def setup(bot):
    bot.add_cog(Purge(bot))
