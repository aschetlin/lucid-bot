import asyncio

import discord
from discord.ext import commands
from discord.utils import get


class Moderation(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *args):
        if not args:
            embed = discord.Embed(
                title="Channel Slowmode -",
                description="How long should the message cool-down be?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    slowmodeTime = await self.bot.wait_for(
                        "message", timeout=20
                    )

                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Timeout Error -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if slowmodeTime.author.id == ctx.author.id:
                    await slowmodeTime.delete()
                    await ctx.channel.edit(
                        slowmode_delay=slowmodeTime.content
                    )
                    print(ctx.channel.slowmode_delay)

                    embed = discord.Embed(
                        title="Channel Slowmode -",
                        description=f"{slowmodeTime.content}s slowmode activated!",
                    )

                    await message.edit(embed=embed)

                    return None

        if str(args[0]) == "lift":
            await ctx.channel.edit(slowmode_delay=0)

            embed = discord.Embed(
                title="Channel Slowmode -", description="Slowmode lifted!"
            )
            await ctx.send(embed=embed)

        else:

            try:
                slowmodeTime = args[0]

                await ctx.channel.edit(slowmode_delay=slowmodeTime)

                embed = discord.Embed(
                    title="Channel Slowmode -",
                    description=f"{slowmodeTime}s slowmode activated!",
                )
                await ctx.send(embed=embed)

            except IndexError:
                embed = discord.Embed(
                    title="Channel Slowmode -",
                    description="Invalid slowmode time.",
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *args):
        if not args:
            embed = discord.Embed(
                title="Punishment -",
                description="Which user should be kicked?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    kickUser = await self.bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if kickUser.author.id == ctx.author.id:
                    await kickUser.delete()
                    try:
                        await kickUser.mentions[0].ban()

                        embed = discord.Embed(
                            title="Successfully banned user -",
                            description=kickUser.mentions[0].mention,
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = discord.Embed(
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = discord.Embed(
                            title="Permissions Error -",
                            description="Are you trying to kick another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                targetUser = ctx.message.mentions[0]
                await targetUser.kick()

            except IndexError:
                embed = discord.Embed(
                    title="Punishment Failed -",
                    description="IndexError: Did you mention a valid "
                    "user?",
                )
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = discord.Embed(
                    title="Permissions Error -",
                    description="Are you trying to kick another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *args):
        if not args:
            embed = discord.Embed(
                title="Punishment -",
                description="Which user should be banned?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    banUser = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if banUser.author.id == ctx.author.id:
                    await banUser.delete()
                    try:
                        await banUser.mentions[0].ban()

                        embed = discord.Embed(
                            title="Successfully banned user -",
                            description=banUser.mentions[0].mention,
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = discord.Embed(
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = discord.Embed(
                            title="Permissions Error -",
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                targetUser = ctx.message.mentions[0]
                await targetUser.ban()

            except IndexError:
                embed = discord.Embed(
                    title="Punishment Failed -",
                    description="IndexError: Did you mention a valid "
                    "user?",
                )
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = discord.Embed(
                    title="Permissions Error -",
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, *args):

        if not args:
            embed = discord.Embed(
                title="Punishment -",
                description="Which user should be muted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    muteMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = discord.Embed(
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

                        embed = discord.Embed(
                            title="Successfully muted user -",
                            description=muteMsg.mentions[0].mention,
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = discord.Embed(
                            title="Punishment Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = discord.Embed(
                            title="Permissions Error -",
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

        embed = discord.Embed(
            title="Message Purge -",
            description=f"Successfully purged {amount} messages.",
        )
        await ctx.send(embed=embed)
