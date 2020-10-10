import discord
from discord.ext import commands
import json
import asyncio

# BOT INIT

config = json.loads(open("json/config.json", "r", encoding="utf8").read())
ticketcount = json.loads(open("json/ticketcount.json", "r").read())
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=False, intents=intents)


def save_json():
    with open('json/ticketcount.json', 'w') as jsonFile:
        json.dump(ticketcount, jsonFile)


@bot.event
async def on_ready():
    print(config["botName"] + " " + "bot online\n---")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Command Error -", description="Command not found.")
        await ctx.send(embed=embed)

    else:
        raise error


async def yes_no_dialogue(message_name: discord.Message, timeout: int, dm: bool, ctx) -> object:
    await message_name.add_reaction("✅")
    await message_name.add_reaction("❌")

    while True:

        try:
            reaction = await bot.wait_for("reaction_add", timeout=timeout)

        except asyncio.TimeoutError:
            embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to react.")

            if dm:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send(embed=embed)

            return None

        if reaction[1].id == ctx.author.id:
            reaction = reaction[0].emoji

            if reaction == "✅" or "❌":
                break

            else:
                return None

    if reaction == "✅":
        return True
    else:
        return False


@bot.command(aliases=["issue"])
async def report(ctx):
    embed = discord.Embed(title="Issue Report -", description="Issue report started in your dms!")
    await ctx.send(embed=embed)

    embed = discord.Embed(title="Issue Report -", description="Would you like to start an issue report ticket?")
    message = await ctx.author.send(embed=embed)

    startTicket = await yes_no_dialogue(message, 30, True, ctx)

    if startTicket:

        embed = discord.Embed(title="Issue Report -", description="What should the title of your issue be?")
        await ctx.author.send(embed=embed)

        while True:

            try:
                issueTitle = await bot.wait_for("message", timeout=20)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
                await ctx.author.send(embed=embed)

                return None

            if issueTitle.author.id == ctx.author.id:
                break

        while True:

            embed = discord.Embed(title="Issue Report -", description="Describe your issue as detailed as possible, "
                                                                      "and how to recreate it, (if applicable).")
            await ctx.author.send(embed=embed)

            try:
                issueDescription = await bot.wait_for("message", timeout=120)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
                await ctx.author.send(embed=embed)

                return None

            if issueDescription.author.id == ctx.author.id:
                embed = discord.Embed(title="Issue Report -", description="Issue report successfully filed, thank you!",
                                      color=0x00fe5f)
                await ctx.author.send(embed=embed)

                user = bot.get_user(581593263736356885)

                await user.send("**Issue Ticket #" + str(ticketcount[config["token"]]) + " - **")

                embed = discord.Embed(title=str(issueTitle.content), description=str(issueDescription.content))
                embed.set_footer(text=str(ctx.author) + " - " + str(ctx.author.id))

                await user.send(embed=embed)

                ticketcount[config["token"]] += 1

                break

    else:
        embed = discord.Embed(title="Issue Report -", description="Ticket creation cancelled.")
        await ctx.author.send(embed=embed)

    save_json()


@bot.command(aliases=["announcement"])
async def announce(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.id in config["adminIDS"]:

        # EMBED CHANNEL
        embed = discord.Embed(
            title="Bot Announcement -", description="What channel should the announcement be sent to?"
        )

        message = await ctx.send(embed=embed)

        while True:

            try:
                announceChannel = await bot.wait_for("message", timeout=20)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
                await message.edit(embed=embed)

                return None

            if announceChannel.author.id == ctx.author.id:
                await announceChannel.delete()
                channelTag = announceChannel.content

                try:
                    announceChannel = announceChannel.channel_mentions[0]

                except IndexError:
                    embed = discord.Embed(title="Command Error -", description="Did you mention a valid channel?")
                    await message.edit(embed=embed)

                    return None

                break

        # EMBED TITLE
        embed = discord.Embed(title="Bot Announcement -", description="What should the title of the announcement be?")

        await message.edit(embed=embed)

        while True:

            try:
                announceTitle = await bot.wait_for("message", timeout=60)


            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")

                await message.edit(embed=embed)

                return None

            if announceTitle.author.id == ctx.author.id:
                await announceTitle.delete()

                break

        # EMBED DESCRIPTION
        embed = discord.Embed(title="Bot Announcement -", description="What should the announcement say?")

        await message.edit(embed=embed)

        while True:

            try:
                announceMessage = await bot.wait_for("message", timeout=180)


            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")

                await message.edit(embed=embed)

                return None

            if announceMessage.author.id == ctx.author.id:
                await announceMessage.delete()

                break

        # EMBED COLOR
        embed = discord.Embed(title="Bot Announcement -",
                              description="What should the color of the embed be?\n\n(Wait for all reactions to "
                                          "appear.)")

        await message.edit(embed=embed)

        for value in config["reactColors"]:
            await message.add_reaction(config["reactColors"][value])

        while True:

            try:
                reactColor = await bot.wait_for("reaction_add", timeout=20)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to react.")

                await message.edit(embed=embed)

                return None

            if reactColor[1].id == ctx.author.id:
                reactColor = reactColor[0].emoji

                if reactColor in config["reactColors"].values():
                    break

                else:
                    return None

        colorHex = config["reactColorsHex"][reactColor]

        # ANNOUNCEMENT AUTHOR YES/NO

        embed = discord.Embed(title="Should the announcement list who created it in the footer,\n"
                                    "eg. the footer of this message?")
        embed.set_footer(text="announcement from " + str(ctx.author))

        await message.clear_reactions()

        await message.edit(embed=embed)

        reaction_yes = await yes_no_dialogue(message, 10, False, ctx)

        # BUILDING ANNOUNCEMENT EMBED
        hexInt = int(colorHex, 16)
        announceEmbed = discord.Embed(title=announceTitle.content, description=announceMessage.content,
                                      color=hexInt)

        if reaction_yes:
            announceEmbed.set_footer(text="announcement from " + str(ctx.author))

        await message.clear_reactions()

        await message.edit(embed=announceEmbed)

        # CONFIRM/DENY SEND
        embed = discord.Embed(title="Bot Announcement -", description="Do you want to send the announcement " +
                                                                      "as shown above?")
        message = await ctx.send(embed=embed)

        reaction_yes = await yes_no_dialogue(message, 10, False, ctx)

        if reaction_yes:
            await announceChannel.send(embed=announceEmbed)
            embed = discord.Embed(title="Bot Announcement -",
                                  description="Announcement successfully sent to " + channelTag + ".")
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)
        else:
            embed = discord.Embed(title="Bot Announcement -",
                                  description="Announcement Cancelled.")
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="Sorry, you don't have the required "
                                                                       "permissions to execute that command.")
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
                    embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
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
                    banUser = await bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
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


@bot.command(aliases=["raid", "panic"])
async def lockdown(ctx, *args):
    if ctx.author.guild_permissions.manage_channels or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Channel Lockdown -", description="Should all channels or only this channel be "
                                                                          "locked down?\n\n (Yes for all channels, "
                                                                          "no for this channel only.)")
            message = await ctx.send(embed=embed)

            allChannels = await yes_no_dialogue(message, 20, False, ctx)

            if allChannels:
                text_channel_list = []
                guild = ctx.guild

                for channel in guild.text_channels:
                    text_channel_list.append(channel)

                for channel in text_channel_list:
                    await channel.set_permissions(ctx.guild.default_role, send_messages=False)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel lockdown successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

            else:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel lockdown successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

        elif args[0] == "lift".lower():

            embed = discord.Embed(title="Channel Lockdown -", description="Should all channels or only this channel "
                                                                          "be unlocked? \n\n (Yes for all channels, "
                                                                          "no for this channel only.)")
            message = await ctx.send(embed=embed)

            allChannels = await yes_no_dialogue(message, 20, False, ctx)

            if allChannels:
                text_channel_list = []
                guild = ctx.guild

                for channel in guild.text_channels:
                    text_channel_list.append(channel)

                for channel in text_channel_list:
                    await channel.set_permissions(ctx.guild.default_role, send_messages=True)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel unlock successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

            else:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel unlock successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

        else:
            embed = discord.Embed(title="Command Failed", description="Unknown argument, \"" + args[0] + "\"")
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None


bot.run(config["token"])
