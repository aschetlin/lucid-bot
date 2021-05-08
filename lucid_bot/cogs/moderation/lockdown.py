from discord.ext import commands
from lucid_bot import utils
from lucid_bot.lucid_embed import lucid_embed


class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = utils.Utils(bot)

    @commands.command(name="lockdown")
    @commands.has_permissions(manage_guild=True)
    async def _lockdown(self, ctx, args="lock"):
        if args == "lock":
            await ctx.channel.set_permissions(
                ctx.guild.default_role, send_messages=False
            )
            await self.utils.command_success(ctx, react=True)

        elif args == "lift":
            await ctx.channel.set_permissions(
                ctx.guild.default_role, send_messages=True
            )
            await self.utils.command_success(ctx, react=True)

        else:
            raise commands.CommandNotFound


def setup(bot):
    bot.add_cog(Lockdown(bot))
