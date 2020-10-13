import discord
import redis
import asyncio
from lucid_bot.config import config
from lucid_bot.non_bot_funcs import yes_no_dialogue, announcement_init, announcement_send
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
async def announce(ctx, *args):
    if ctx.author.guild_permissions.administrator or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(
                title="Bot Announcement -", description="What channel should the announcement be sent to?")

            message = await ctx.send(embed=embed)

            announceChannel, announceTitle, channelTag = await announcement_init(ctx, message)

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

            await announcement_send(ctx, announceChannel, announceEmbed, channelTag)

        elif args[0].lower() == "image":
            embed = discord.Embed(
                title="Bot Announcement -", description="What channel should the announcement be sent to?")

            message = await ctx.send(embed=embed)

            announceChannel, announceTitleMessage, channelTag = await announcement_init(ctx, message)

            announceTitle = announceTitleMessage.content

            embed = discord.Embed(title="Bot Announcement -", description="Please link the image url.")
            await message.edit(embed=embed)

            while True:

                try:
                    image = await bot.wait_for("message", timeout=40)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout Error -", description="Sorry, you took too long to respond.")
                    await message.edit(embed=embed)

                    return None

                if image.author.id == ctx.author.id:
                    break

            announceEmbed = discord.Embed(title=announceTitle)
            announceEmbed.set_image(url=image.content)

            await ctx.send(embed=announceEmbed)

            await announcement_send(ctx, announceChannel, announceEmbed, channelTag)

    else:
        embed = discord.Embed(title="Permissions Error -", description="Sorry, you don't have the required "
                                                                       "permissions to execute that command.")
        await ctx.send(embed=embed)
