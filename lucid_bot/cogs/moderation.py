import discord
from discord.ext import commands
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf

    @commands.command()
    async def slowmode(self, ctx, *args):
        if ctx.author.guild_permissions.manage_channels:

            if not args:
                embed = discord.Embed(title="Channel Slowmode -", description="How long should the message cool-down be?")
                message = await ctx.send(embed=embed)

                while True:

                    try:
                        slowmodeTime = await self.bot.wait_for("message", timeout=20)

                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="Timeout Error -", description="Sorry, you took too long to respond.")
                        await message.edit(embed=embed)

                        return None

                    if slowmodeTime.author.id == ctx.author.id:
                        await slowmodeTime.delete()
                        await ctx.channel.edit(slowmode_delay=slowmodeTime.content)
                        print(ctx.channel.slowmode_delay)

                        embed = discord.Embed(title="Channel Slowmode -",
                                            description=f"{slowmodeTime.content}s slowmode activated!")

                        await message.edit(embed=embed)

                        return None

            if str(args[0]) == "lift":
                await ctx.channel.edit(slowmode_delay=0)

                embed = discord.Embed(title="Channel Slowmode -", description="Slowmode lifted!")
                await ctx.send(embed=embed)

            else:

                try:
                    slowmodeTime = args[0]

                    await ctx.channel.edit(slowmode_delay=slowmodeTime)

                    embed = discord.Embed(title="Channel Slowmode -", description=f"{slowmodeTime}s slowmode activated!")
                    await ctx.send(embed=embed)

                except IndexError:
                    embed = discord.Embed(title="Channel Slowmode -", description="Invalid slowmode time.")
                    await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Permissions Error -", description="You don't have the required permissions to "
                                                                        "execute that command.")
            await ctx.send(embed=embed)


    @commands.command()
    async def kick(self, ctx, *args):
        if ctx.author.guild_permissions.kick_members or ctx.author.id in self.config["adminIDS"]:

            if not args:
                embed = discord.Embed(title="Punishment -", description="Which user should be kicked?")
                message = await ctx.send(embed=embed)

                while True:

                    try:
                        kickUser = await self.bot.wait_for("message", timeout=20)

                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to respond.")
                        await message.edit(embed=embed)

                        return None

                    if kickUser.author.id == ctx.author.id:
                        await kickUser.delete()
                        try:
                            await kickUser.mentions[0].ban()

                            embed = discord.Embed(
                                title="Successfully banned user -", description=kickUser.mentions[0].mention
                            )
                            await message.edit(embed=embed)

                            return None

                        except IndexError:
                            embed = discord.Embed(title="Punishment Failed -", description="Did you mention a user?")
                            await message.edit(embed=embed)

                            return None

                        except discord.errors.Forbidden:
                            embed = discord.Embed(title="Permissions Error -", description="Are you trying to kick another "
                                                                                        "moderator/administrator?")
                            await message.edit(embed=embed)

                            return None

            else:

                try:
                    targetUser = ctx.message.mentions[0]
                    await targetUser.kick()

                except IndexError:
                    embed = discord.Embed(title="Punishment Failed -", description="IndexError: Did you mention a valid "
                                                                                "user?")
                    await ctx.send(embed=embed)

                except discord.Forbidden:
                    embed = discord.Embed(title="Permissions Error -", description="Are you trying to kick another "
                                                                                "moderator/administrator?")
                    await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                        "permissions to execute this command.")
            await ctx.send(embed=embed)

            return None


    @commands.command()
    async def ban(self, ctx, *args):
        if ctx.author.guild_permissions.ban_members or ctx.author.id in self.config["adminIDS"]:

            if not args:
                embed = discord.Embed(title="Punishment -", description="Which user should be banned?")
                message = await ctx.send(embed=embed)

                while True:

                    try:
                        banUser = await self.bot.wait_for("message", timeout=15)

                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to respond.")
                        await message.edit(embed=embed)

                        return None

                    if banUser.author.id == ctx.author.id:
                        await banUser.delete()
                        try:
                            await banUser.mentions[0].ban()

                            embed = discord.Embed(
                                title="Successfully banned user -", description=banUser.mentions[0].mention
                            )
                            await message.edit(embed=embed)

                            return None

                        except IndexError:
                            embed = discord.Embed(title="Punishment Failed -", description="Did you mention a user?")
                            await message.edit(embed=embed)

                            return None

                        except discord.errors.Forbidden:
                            embed = discord.Embed(title="Permissions Error -", description="Are you trying to ban another "
                                                                                        "moderator/administrator?")
                            await message.edit(embed=embed)

                            return None

            else:

                try:
                    targetUser = ctx.message.mentions[0]
                    await targetUser.ban()

                except IndexError:
                    embed = discord.Embed(title="Punishment Failed -", description="IndexError: Did you mention a valid "
                                                                                "user?")
                    await ctx.send(embed=embed)

                except discord.Forbidden:
                    embed = discord.Embed(title="Permissions Error -", description="Are you trying to ban another "
                                                                                "moderator/administrator?")
                    await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                        "permissions to execute this command.")
            await ctx.send(embed=embed)

            return None


    @commands.command()
    async def purge(self, ctx, amount=5):
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=amount + 1)

            embed = discord.Embed(title="Message Purge -", description=f"Successfully purged {amount} messages.")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                        "permissions to execute this command.")
            await ctx.send(embed=embed)