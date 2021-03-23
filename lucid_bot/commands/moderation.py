import discord
import asyncio

from lucid_bot.bot import bot
from lucid_bot.config import config
from lucid_bot.non_bot_funcs import yes_no_dialogue # noqa


@bot.command()
async def slowmode(ctx, *args):
    if ctx.author.guild_permissions.manage_channels:

        if not args:
            embed = discord.Embed(title="Channel Slowmode -", description="How long should the message cool-down be?")
            message = await ctx.send(embed=embed)

            while True:

                try:
                    slowmodeTime = await bot.wait_for("message", timeout=20)

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


@bot.command()
async def kick(ctx, *args):
    if ctx.author.guild_permissions.kick_members or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Punishment -", description="Which user should be kicked?")
            message = await ctx.send(embed=embed)

            while True:

                try:
                    kickUser = await bot.wait_for("message", timeout=20)

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


@bot.command()
async def ban(ctx, *args):
    if ctx.author.guild_permissions.ban_members or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Punishment -", description="Which user should be banned?")
            message = await ctx.send(embed=embed)

            while True:

                try:
                    banUser = await bot.wait_for("message", timeout=15)

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


@bot.command()
async def purge(ctx, amount=5):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount + 1)

        embed = discord.Embed(title="Message Purge -", description=f"Successfully purged {amount} messages.")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)


@bot.command()
async def lockdown(ctx, args):
    if ctx.author.guild_permissions.administrator:

        if not args:
            embed = discord.Embed(title="Channel Lockdown -", description="Are you sure you want to lockdown this "
                                                                          "channel?")
            message = await ctx.send(embed=embed)

           # if yes_no_dialogue(message, 20, False, ctx):






        if args[0] == "lift":
            embed = discord.Embed(title="Channel Lockdown -", desciption="Are you sure you want to lift the lockdown "
                                                                         "on this channel?")

            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You don't have the required permissions to "
                                                                       "execute that command.")
        await ctx.send(embed=embed)



