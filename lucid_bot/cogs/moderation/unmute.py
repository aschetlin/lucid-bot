import asyncio

import discord
from discord.ext import commands
from discord.utils import get
from lucid_bot.embed import embed


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, *args):

        if not args:
            embed = embed(
                ctx,
                title="Punishment -",
                description="Which user should be unmuted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    unmuteMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = embed(
                        ctx,
                        success=False,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if unmuteMsg.author.id == ctx.author.id:

                    await unmuteMsg.delete()

                    try:
                        role = get(unmuteMsg.mentions[0].roles, name="Muted")

                        await unmuteMsg.mentions[0].remove_roles(role)
                        await ctx.message.delete()

                        embed = embed(ctx, success=True).set_author(
                            name=f"| Successfully unmuted {unmuteMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = embed(
                            ctx,
                            success=False,
                            title="Command Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = embed(
                            ctx,
                            success=False,
                            title="Permissions Error -",
                            description="Are you trying to unmute another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None
        else:
            await ctx.message.delete()

            try:
                role = get(ctx.message.mentions[0].roles, name="Muted")

                await ctx.message.mentions[0].remove_roles(role)

                embed = embed(ctx, success=True).set_author(
                    name=f"| Successfully unmuted {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = embed(
                    ctx,
                    success=False,
                    title="Command Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = embed(
                    ctx,
                    success=False,
                    title="Permissions Error -",
                    description="Are you trying to unmute another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None
