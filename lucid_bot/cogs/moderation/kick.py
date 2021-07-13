import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx: commands.Context, *args) -> None:
        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be kicked?",
            )
            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    kick_user_message: discord.Message = await self.bot.wait_for(
                        "message", timeout=20
                    )

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if kick_user_message.author.id == ctx.author.id:
                    await kick_user_message.delete()

                    try:
                        await kick_user_message.mentions[0].kick()
                        await message.delete()

                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.SUCCESS,
                        )

                        return None

                    except IndexError:
                        await message.delete()
                        await kick_user_message.delete()

                        await self.utils.command_result(
                            ctx, result=LucidCommandResult.FAIL
                        )

                        return None

                    except discord.errors.Forbidden:
                        await message.delete()
                        await kick_user_message.delete()

                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.FAIL,
                        )

                        return None

        else:

            try:
                await ctx.message.mentions[0].kick()
                await ctx.message.delete()

                await self.utils.command_result(
                    ctx,
                    result=LucidCommandResult.SUCCESS,
                )

                return None

            except IndexError:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

            except discord.Forbidden:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)


def setup(bot):
    bot.add_cog(Kick(bot))
