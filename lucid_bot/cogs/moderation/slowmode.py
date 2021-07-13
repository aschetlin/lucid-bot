import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.group(name="slowmode", invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, ctx: commands.Context, time: int = None) -> None:
        if not time:

            embed = lucid_embed(
                ctx,
                title="Channel Slowmode -",
                description="How long should the message cool-down be?",
            )
            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    slowmodeTime = await self.bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout Error -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if slowmodeTime.author.id == ctx.author.id:
                    await slowmodeTime.delete()
                    await ctx.channel.edit(slowmode_delay=slowmodeTime.content)

                    await message.delete()
                    await self.utils.command_result(
                        ctx, result=LucidCommandResult.SUCCESS
                    )

                    return None
        else:

            try:
                slowmodeTime = time

                await ctx.channel.edit(slowmode_delay=slowmodeTime)
                await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)

            except IndexError:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

    @_slowmode.command(name="lift")
    async def _slowmode_lift(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)


def setup(bot):
    bot.add_cog(Slowmode(bot))
