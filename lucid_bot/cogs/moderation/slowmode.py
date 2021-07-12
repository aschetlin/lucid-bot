import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed


class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
                    await ctx.message.add_reaction("✅")

                    return None
        else:

            try:
                slowmodeTime = time

                await ctx.channel.edit(slowmode_delay=slowmodeTime)
                await ctx.message.add_reaction("✅")

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Channel Slowmode -",
                    description="Invalid slowmode time.",
                )
                await ctx.send(embed=embed)

    @_slowmode.command(name="lift")
    async def _slowmode_lift(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Slowmode(bot))
