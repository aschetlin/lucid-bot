import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx: commands.Context, *args) -> None:
        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be banned?",
            )
            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    ban_user_message: discord.Message = await self.bot.wait_for(
                        "message", timeout=15
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

                if ban_user_message.author.id == ctx.author.id:
                    await ban_user_message.delete()
                    try:
                        await ban_user_message.mentions[0].ban()

                        await message.delete()
                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.SUCCESS,
                        )

                        return None

                    except IndexError:
                        await message.delete()
                        await ban_user_message.delete()

                        await self.utils.command_result(
                            ctx, result=LucidCommandResult.FAIL
                        )

                        return None

                    except discord.errors.Forbidden:
                        await message.delete()
                        await ban_user_message.delete()

                        await self.utils.command_result(
                            ctx, result=LucidCommandResult.FAIL
                        )

                        return None

        else:

            try:
                await ctx.message.mentions[0].ban()
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
    bot.add_cog(Ban(bot))
