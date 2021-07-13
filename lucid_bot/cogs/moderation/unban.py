import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed
from lucid_bot.utils import Utils, LucidCommandResult


class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx: commands.Context, *args) -> None:
        if not args:
            embed = lucid_embed(
                ctx,
                title="Unban -",
                description="Which user should be unbanned?",
            )
            message: discord.Message = await ctx.send(embed=embed)

            while True:

                try:
                    unban_message: discord.Message = await self.bot.wait_for(
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

                if unban_message.author.id == ctx.author.id:
                    await unban_message.delete()
                    try:
                        unban_user: discord.User = await self.bot.fetch_user(
                            int(unban_message.content)
                        )
                        await ctx.guild.unban(unban_user)

                        await message.delete()
                        await self.utils.command_result(
                            ctx,
                            result=LucidCommandResult.SUCCESS,
                        )

                        return None

                    # except IndexError:
                    #     embed = Embed(
                    #         ctx,
                    #         fail=True,
                    #         title="Unban Failed -",
                    #         description="Did you mention a user?",
                    #     )
                    #     await message.edit(embed=embed)

                    #     return None

                    except discord.errors.Forbidden:
                        await message.delete()
                        await ctx.message.delete()

                        await self.utils.command_result(
                            ctx, result=LucidCommandResult.FAIL
                        )

                        return None
        else:

            try:
                await ctx.message.mentions[0].unban()
                await ctx.message.delete()

                await self.utils.command_result(
                    ctx,
                    result=LucidCommandResult.SUCCESS,
                )

                return None

            except IndexError:
                await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

            # except discord.Forbidden:
            #     embed = Embed(
            #         ctx,
            #         fail=True,
            #         title="Permissions Error -",
            #         description="Are you trying to ban another "
            #         "moderator/administrator?",
            #     )
            #     await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Unban(bot))
