from discord.ext import commands
from lucid_bot.utils import Utils, LucidCommandResult


class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.group(name="lockdown", invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def _lockdown(self, ctx: commands.Context) -> None:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)

    @_lockdown.command(name="lift")
    async def _lockdown_lift(self, ctx: commands.Context) -> None:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)


def setup(bot):
    bot.add_cog(Lockdown(bot))
