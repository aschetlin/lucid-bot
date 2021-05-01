import asyncio
import datetime

import discord


class NonBotFuncs:
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    def time(self):
        time = datetime.now().strftime("%H:%M:%S:$f")
        return f"[\033[32m{time[:12]}\033[0m] |"

    async def yes_no_dialogue(
        self, message_name: discord.Message, timeout: int, dm: bool, ctx
    ) -> object:
        await message_name.add_reaction("✅")
        await message_name.add_reaction("❌")

        while True:

            try:
                reaction = await self.bot.wait_for(
                    "reaction_add", timeout=timeout
                )

            except asyncio.TimeoutError:
                embed = embed(
                    title="Timeout -",
                    description="Sorry, you took too long to react.",
                )

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

    async def announcement_channel(self, ctx, message: discord.Message):
        # EMBED CHANNEL
        while True:

            try:
                announceChannel = await self.bot.wait_for(
                    "message", timeout=20
                )

            except asyncio.TimeoutError:
                embed = embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )
                await message.edit(embed=embed)

                return None

            if announceChannel.author.id == ctx.author.id:
                await announceChannel.delete()
                channelTag = announceChannel.content

                try:
                    announceChannel = announceChannel.channel_mentions[0]

                except IndexError:
                    embed = embed(
                        title="Command Error -",
                        description="Did you mention a valid channel?",
                    )
                    await message.edit(embed=embed)

                    return None

                break

        return announceChannel, channelTag

    async def announce_title(self, ctx, message: discord.Message):
        # EMBED TITLE
        embed = embed(
            title="Bot Announcement -",
            description="What should the title of the announcement be?",
        )

        await message.edit(embed=embed)

        while True:

            try:
                announceTitle = await self.bot.wait_for("message", timeout=60)

            except asyncio.TimeoutError:
                embed = embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )

                await message.edit(embed=embed)

                return None

            if announceTitle.author.id == ctx.author.id:
                await announceTitle.delete()

                break

        return announceTitle.content

    async def announcement_description(self, ctx, message: discord.Message):
        # EMBED DESCRIPTION
        embed = embed(
            title="Bot Announcement -",
            description="What should the announcement say?",
        )

        await message.edit(embed=embed)

        while True:

            try:
                announceMessage = await self.bot.wait_for(
                    "message", timeout=180
                )

            except asyncio.TimeoutError:
                embed = embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )

                await message.edit(embed=embed)

                return None

            if announceMessage.author.id == ctx.author.id:
                await announceMessage.delete()

                break

        return announceMessage.content

    async def announce_color(self, message, ctx):
        embed = embed(
            title="Bot Announcement -",
            description="What should the color of the embed be?\n\n(Wait for all reactions to "
            "appear.)",
        )

        await message.edit(embed=embed)

        for value in self.config["reactColors"]:
            await message.add_reaction(self.config["reactColors"][value])

        while True:

            try:
                reactColor = await self.bot.wait_for(
                    "reaction_add", timeout=20
                )

            except asyncio.TimeoutError:
                embed = embed(
                    title="Timeout -",
                    description="Sorry, you took too long to react.",
                )

                await message.edit(embed=embed)

                return None

            if reactColor[1].id == ctx.author.id:
                reactColor = reactColor[0].emoji

                if reactColor in self.config["reactColors"].values():
                    break

                else:
                    return None

        colorHex = self.config["reactColorsHex"][reactColor]
        return str(colorHex)

    async def announcement_send(
        self, ctx, announce_channel, announce_embed, channel_tag
    ):
        # CONFIRM/DENY SEND
        embed = embed(
            title="Bot Announcement -",
            description="Do you want to send the announcement "
            + "as shown above?",
        )
        message = await ctx.send(embed=embed)

        reaction_yes = await self.yes_no_dialogue(message, 10, False, ctx)

        if reaction_yes:
            await announce_channel.send(embed=announce_embed)
            embed = embed(
                title="Bot Announcement -",
                description="Announcement successfully sent to "
                + channel_tag
                + ".",
            )
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)

        else:
            embed = embed(
                title="Bot Announcement -",
                description="Announcement Cancelled.",
            )
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)

        return
