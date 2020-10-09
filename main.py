import discord
from discord.ext import commands
import json
import asyncio

# CONSTANTS BELOW

# intents = discord.Intents.default()
# intents.members = True

adminIDS = [
    "581593263736356885"  # viargentum#3850
    "530540004082974720"  # Rune - Vega Development#8717
]

reactColors = {

    "red": "❤",
    "orange": "🧡",
    "yellow": "💛",
    "green": "💚",
    "blue": "💙",
    "purple": "💜",
    "black": "🖤",
    "brown": "🤎",
    "white": "🤍"

}

reactColorsHex = {

    "❤": 0xff0000,
    "🧡": 0xFFA500,
    "💛": 0xFFFF00,
    "💚": 0x008000,
    "💙": 0x0000FF,
    "💜": 0x800080,
    "🖤": 0x000000,
    "🤎": 0x512525,
    "🤍": 0xFFFFFF

}

helloResponseOptions = [

    "hi",
    "hii",
    "hello",
    "heyy"

]

ticketcount = json.loads(open("json/ticketcount.json", "r").read())
token = json.loads(open("json/token.json", "r").read())

bot = commands.Bot(command_prefix="\\", case_insensitive=False)


def save_json():
    with open('json/ticketcount.json', 'w') as jsonFile:
        json.dump(ticketcount, jsonFile)


@bot.event
async def on_ready():
    print("vega bot online\n---")


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

                user = ctx.message.guild.get_member(581593263736356885)

                await user.send("**Issue Ticket #" + str(ticketcount["tickets"]) + " - **")

                embed = discord.Embed(title=str(issueTitle.content), description=str(issueDescription.content))
                embed.set_footer(text=str(ctx.author) + " - " + str(ctx.author.id))

                await user.send(embed=embed)

                ticketcount["tickets"] += 1

                break

    else:
        embed = discord.Embed(title="Issue Report -", description="Ticket creation cancelled.")
        await ctx.author.send(embed=embed)

    save_json()


@bot.command(aliases=["announcement"])
async def announce(ctx):
    if ctx.author.guild_permissions.administrator:

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

            except IndexError:
                embed = discord.Embed(title="Error:",
                                      description="You did not specify a valid channel.\n\nMake sure you mention the "
                                                  "channel by using a # before the channel name.")
                await message.edit(embed=embed)

                return None

            if announceChannel.author.id == ctx.author.id:
                await announceChannel.delete()
                channelTag = announceChannel.content
                announceChannel = announceChannel.channel_mentions[0]

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

        for keys in reactColors:
            await message.add_reaction(reactColors[keys])

        while True:

            try:
                reactColor = await bot.wait_for("reaction_add", timeout=20)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout", description="Sorry, you took too long to react.")

                await message.edit(embed=embed)

                return None

            if reactColor[1].id == ctx.author.id:
                reactColor = reactColor[0].emoji

                if reactColor in reactColors.values():
                    break

                else:
                    return None

        colorHex = reactColorsHex[reactColor]

        # ANNOUNCEMENT AUTHOR YES/NO

        embed = discord.Embed(title="Should the announcement list who created it in the footer,\n"
                                    "eg. the footer of this message?")
        embed.set_footer(text="announcement from " + str(ctx.author))

        await message.clear_reactions()

        await message.edit(embed=embed)

        reaction_yes = await yes_no_dialogue(message, 10, False, ctx)

        # BUILDING ANNOUNCEMENT EMBED
        announceEmbed = discord.Embed(title=announceTitle.content, description=announceMessage.content,
                                      color=colorHex)

        if reaction_yes:
            announceEmbed.set_footer(text="announcement from " + str(ctx.author))
        else:
            return None

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
async def kick(ctx):
    if ctx.author.guild_permissions.kick_members:

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
                    await kickUser.mentions[0].kick()

                    embed = discord.Embed(title="Successfully kicked user -", description=kickUser.mentions[0].mention)
                    await message.edit(embed=embed)

                except discord.errors.Forbidden:
                    embed = discord.Embed(title="Punishment Failed -", description="Return error: `Permissions "
                                                                                   "Error`\n\n "
                                                                                   "Are you trying to kick another "
                                                                                   "moderator/administrator?")
                    await message.edit(embed=embed)

                    return None
    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None


@bot.command()
async def ban(ctx):
    if ctx.author.guild_permissions.ban_members:

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

                    embed = discord.Embed(title="Successfully banned user -", description=banUser.mentions[0].mention)
                    await message.edit(embed=embed)

                except discord.errors.Forbidden:
                    embed = discord.Embed(title="Punishment Failed -", description="Return error: `Permissions "
                                                                                   "Error`\n\n "
                                                                                   "Are you trying to ban another "
                                                                                   "moderator/administrator?")
                    await message.edit(embed=embed)

                    return None
    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None


bot.run(token["token"])
