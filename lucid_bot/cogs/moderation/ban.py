import asyncio

import discord
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx: commands.Context, *args) -> None:
        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be banned?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    banUser = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if banUser.author.id == ctx.author.id:
                    await banUser.delete()
                    try:
                        await banUser.mentions[0].ban()

                        embed = lucid_embed(ctx, success=True).set_author(
                            name=f"| Successfully banned {banUser.mentions[0]}.",
                            icon_url="https://imgur.com/a/RvkKizk",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Permissions Error -",
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                await ctx.message.mentions[0].ban()
                await ctx.message.delete()

                embed = lucid_embed(ctx, success=True).set_author(
                    name=f"| Successfully banned {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Punishment Failed -",
                    description="IndexError: Did you mention a valid " "user?",
                )
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Permissions Error -",
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ban(bot))
