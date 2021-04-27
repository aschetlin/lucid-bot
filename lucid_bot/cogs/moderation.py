import asyncio

import discord
from discord import User
from discord.ext import commands
from discord.utils import get
from lucid_bot.embed import Embed


class Moderation(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *args):
        if not args:
            embed = Embed(
                ctx,
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
                    embed = Embed(
                        ctx,
                        success=False,
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

                    embed = Embed(
                        ctx,
                        success=True,
                        title="Channel Slowmode -",
                        description=f"{slowmodeTime.content}s slowmode activated!",
                    )

                    await message.edit(embed=embed)

                    return None

        if str(args[0]) == "lift":
            await ctx.channel.edit(slowmode_delay=0)

            embed = Embed(
                ctx,
                success=True,
                title="Channel Slowmode -", description="Slowmode lifted!"
            )
            await ctx.send(embed=embed)

        else:

            try:
                slowmodeTime = args[0]

                await ctx.channel.edit(slowmode_delay=slowmodeTime)

                embed = Embed(
                    ctx,
                    success=True,
                    title="Channel Slowmode -",
                    description=f"{slowmodeTime}s slowmode activated!",
                )
                await ctx.send(embed=embed)

            except IndexError:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Channel Slowmode -",
                    description="Invalid slowmode time.",
                )
                await ctx.send(embed=embed)

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
                            ctx, success=False,
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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, *args):
        if not args:
            embed = Embed(
                ctx,
                title="Punishment -",
                description="Which user should be banned?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    banUser = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = Embed(
                        ctx,
                        success=False,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if banUser.author.id == ctx.author.id:
                    await banUser.delete()
                    try:
                        await banUser.mentions[0].ban()

                        embed = Embed(ctx, success=True).set_author(
                            name=f"| Successfully banned {banUser.mentions[0]}.",
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
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                await ctx.message.mentions[0].ban()
                await ctx.message.delete()

                embed = Embed(ctx, success=True).set_author(
                    name=f"| Successfully banned {ctx.message.mentions[0]}.",
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
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *args):
        if not args:
            embed = Embed(
                ctx,
                title="Unban -",
                description="Which user should be unbanned?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    unbanMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = Embed(
                        ctx,
                        success=False,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if unbanMsg.author.id == ctx.author.id:
                    await unbanMsg.delete()
                    try:
                        unbanUser = await self.bot.fetch_user(int(unbanMsg.content))
                        await ctx.guild.unban(unbanUser)

                        embed = Embed(ctx, success=True).set_author(
                            name=f"| Successfully unbanned {unbanMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    # except IndexError:
                    #     embed = Embed(
                    #         ctx,
                    #         success=False,
                    #         title="Unban Failed -",
                    #         description="Did you mention a user?",
                    #     )
                    #     await message.edit(embed=embed)

                    #     return None

                    except discord.errors.Forbidden:
                        embed = Embed(
                            ctx,
                            success=False,
                            title="Permissions Error -",
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None
        else:

            try:
                await ctx.message.mentions[0].unban()
                await ctx.message.delete()

                embed = Embed().set_author(
                    ctx,
                    success=True,
                    name=f"| Successfully unbanned {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Unban Failed -",
                    description="IndexError: Did you mention a valid "
                    "user?",
                )
                await ctx.send(embed=embed)

            # except discord.Forbidden:
            #     embed = Embed(
            #         ctx,
            #         success=False,
            #         title="Permissions Error -",
            #         description="Are you trying to ban another "
            #         "moderator/administrator?",
            #     )
            #     await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, *args):

        if not args:
            embed = Embed(
                ctx,
                title="Punishment -",
                description="Which user should be muted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    muteMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = Embed(
                        ctx,
                        success=False,
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

                        embed = Embed(ctx, success=True).set_author(
                            name=f"| Successfully muted {muteMsg.mentions[0]}.",
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

                embed = Embed(ctx, success=True).set_author(
                    name=f"| Successfully muted {muteUser}",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Punishment Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Permissions Error -",
                    description="Are you trying to ban another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, *args):

        if not args:
            embed = Embed(
                ctx,
                title="Punishment -",
                description="Which user should be unmuted?",
            )

            message = await ctx.send(embed=embed)

            while True:

                try:
                    unmuteMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = Embed(
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

                        embed = Embed(ctx, success=True).set_author(
                            name=f"| Successfully unmuted {unmuteMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = Embed(
                            ctx,
                            success=False,
                            title="Command Failed -",
                            description="Did you mention a user?",
                        )
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = Embed(
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

                embed = Embed(ctx, success=True).set_author(
                    name=f"| Successfully unmuted {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Command Failed -",
                    description="Did you mention a user?",
                )
                await ctx.send(embed=embed)

                return None

            except discord.errors.Forbidden:
                embed = Embed(
                    ctx,
                    success=False,
                    title="Permissions Error -",
                    description="Are you trying to unmute another "
                    "moderator/administrator?",
                )
                await ctx.send(embed=embed)

                return None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

        embed = Embed(
            ctx,
            success=True,
            title="Message Purge -",
            description=f"Successfully purged {amount} messages.",
            icon_url="https://i.imgur.com/4yUeOVj.gif",
        )
        await ctx.send(embed=embed)
