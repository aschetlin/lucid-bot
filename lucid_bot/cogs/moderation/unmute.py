import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from lucid_bot.lucid_embed import lucid_embed


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def _unmute(self, ctx, *args):
        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be unmuted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    unmuteMsg = await self.bot.wait_for(
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

                if unmuteMsg.author.id == ctx.author.id:

                    await unmuteMsg.delete()

                    try:
                        role = get(
                            unmuteMsg.mentions[0].roles, name="Muted"
                        )

                        await unmuteMsg.mentions[0].remove_roles(role)
                        await ctx.message.delete()

                        embed = lucid_embed(ctx, success=True).set_author(
                            name=f"| Successfully unmuted {unmuteMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Command Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
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

                embed = lucid_embed(ctx, success=True).set_author(
                    name=f"| Successfully unmuted {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Command Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Permissions Error -",
                    description="Are you trying to unmute another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None


def setup(bot):
    bot.add_cog(Unmute(bot))
