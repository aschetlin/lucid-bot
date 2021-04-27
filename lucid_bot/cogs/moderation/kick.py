import asyncio

import discord
from discord.ext import commands
from lucid_bot.embed import Embed


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *args):

        if not args:
            embed = Embed(
                ctx,
                title="Punishment -",
                description="Which user should be kicked?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    kickUser = await self.bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = Embed(
                        ctx,
                        success=False,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if kickUser.author.id == ctx.author.id:
                    await kickUser.delete()
                    try:
                        await kickUser.mentions[0].kick()

                        embed = Embed(ctx, success=True).set_author(
                            name=f"| Successfully kicked {kickUser.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = Embed(
                            ctx,
                            success=False,
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = Embed(
                            ctx,
                            success=False,
                            title="Permissions Error -",
                            description="Are you trying to kick another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                await ctx.message.mentions[0].kick()
                await ctx.message.delete()

                embed = Embed(ctx, success=True).set_author(
                    name=f"| Successfully kicked {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Punishment Failed -",
                    description="IndexError: Did you mention a valid "
                    "user?",
                )
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Permissions Error -",
                    description="Are you trying to kick another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)
