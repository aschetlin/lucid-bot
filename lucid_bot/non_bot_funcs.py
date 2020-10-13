import asyncio
import discord
from lucid_bot.bot import bot


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


async def announcement_init(ctx, message: discord.Message):
    # EMBED CHANNEL
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

    return announceChannel, announceTitle, channelTag


async def announcement_send(ctx, announce_channel, announce_embed, channel_tag):
    # CONFIRM/DENY SEND
    embed = discord.Embed(title="Bot Announcement -", description="Do you want to send the announcement " +
                                                                  "as shown above?")
    message = await ctx.send(embed=embed)

    reaction_yes = await yes_no_dialogue(message, 10, False, ctx)

    if reaction_yes:
        await announce_channel.send(embed=announce_embed)
        embed = discord.Embed(title="Bot Announcement -",
                              description="Announcement successfully sent to " + channel_tag + ".")
        embed.set_footer(text="bot developed by viargentum#3850")
        await message.clear_reactions()
        await message.edit(embed=embed)
    else:
        embed = discord.Embed(title="Bot Announcement -",
                              description="Announcement Cancelled.")
        embed.set_footer(text="bot developed by viargentum#3850")
        await message.clear_reactions()
        await message.edit(embed=embed)

    return
