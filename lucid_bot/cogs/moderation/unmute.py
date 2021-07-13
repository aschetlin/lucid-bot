import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.command(name="unmute")
    @commands.has_permissions(kick_members=True)
    async def _unmute(self, ctx: commands.Context, *args) -> None:
        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be unmuted?",
            )

            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    unmute_message: discord.Message = await self.bot.wait_for(
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

                if unmute_message.author.id == ctx.author.id:

                    await unmute_message.delete()

                    try:
                        role: discord.Role = get(
                            unmute_message.mentions[0].roles, name="Muted"
                        )

                        await unmute_message.mentions[0].remove_roles(role)
                        await ctx.message.delete()

                        await message.delete()
                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.SUCCESS,
                        )

                        return None

                    except IndexError:
                        await message.delete()
                        await unmute_message.delete()

                        await self.utils.command_result(
                            ctx, result=LucidCommandResult.FAIL
                        )

                        return None

                    except discord.errors.Forbidden:
                        await message.delete()
                        await unmute_message.delete()

                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.FAIL,
                        )

                        return None
        else:
            await ctx.message.delete()

            try:
                role = get(ctx.message.mentions[0].roles, name="Muted")

                await ctx.message.mentions[0].remove_roles(role)

                await self.utils.command_result(
                    ctx,
                    result=LucidCommandResult.SUCCESS,
                )

                return None

            except IndexError:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

                return None

            except discord.errors.Forbidden:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

                return None


def setup(bot):
    bot.add_cog(Unmute(bot))
