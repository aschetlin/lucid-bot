import discord
import redis
import asyncio
from lucid_bot.config import config
from lucid_bot.non_bot_funcs import yes_no_dialogue
from lucid_bot.bot import bot


r = redis.Redis(host=config["redis"]["hostname"], db=config["redis"]["db"])


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
                ticketcount = int(r.get("ticketcount") or 0)

                await user.send(f"**Issue Ticket #{ticketcount} - **")

                embed = discord.Embed(title=str(issueTitle.content), description=str(issueDescription.content))
                embed.set_footer(text=str(ctx.author) + " - " + str(ctx.author.id))

                await user.send(embed=embed)

                r.set("ticketcount", int(ticketcount) + 1)

                break

    else:
        embed = discord.Embed(title="Issue Report -", description="Ticket creation cancelled.")
        await ctx.author.send(embed=embed)


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
