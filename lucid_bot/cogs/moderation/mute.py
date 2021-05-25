import asyncio

import discord
from discord.ext import commands
from discord.utils import get

from lucid_bot.lucid_embed import lucid_embed


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute")
    @commands.is_owner()
    async def _mute(self, ctx, *args):

        if not args:
            embed = lucid_embed(
                ctx,
                title="Punishment -",
                description="Which user should be muted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    muteMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if muteMsg.author.id == ctx.author.id:
                    await muteMsg.delete()
                    permissions = discord.Permissions(send_messages=False)

                    try:
                        role = get(ctx.guild.roles, name="Muted")

                        if not role:
                            role = await ctx.guild.create_role(name="Muted")

                            for channel in ctx.guild.channels:
                                await channel.set_permissions(
                                    role,
                                    send_messages=False,
                                    speak=False,
                                )

                        await muteMsg.mentions[0].add_roles(role)
                        await ctx.message.delete()

                        embed = lucid_embed(ctx, success=True).set_author(
                            name=f"| Successfully muted {muteMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
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
                            description="Are you trying to mute another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None
        else:
            muteUser = ctx.message.mentions[0]
            await ctx.message.delete()

            permissions = discord.Permissions(send_messages=False)

            try:
                role = get(ctx.guild.roles, name="Muted")

                if not role:
                    role = await ctx.guild.create_role(name="Muted")

                    for channel in ctx.guild.channels:
                        await channel.set_permissions(
                            role, send_messages=False, speak=False
                        )

                await muteUser.add_roles(role)

                embed = lucid_embed(ctx, success=True).set_author(
                    name=f"| Successfully muted {muteUser}",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Punishment Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Permissions Error -",
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None


def setup(bot):
    bot.add_cog(Mute(bot))
