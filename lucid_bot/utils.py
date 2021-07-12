import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


class Utils:
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config

    @staticmethod
    def time() -> str:
        time = datetime.now().strftime("%H:%M:%S")
        return f"[\033[32m{time[:12]}\033[0m] | "

    async def command_success(
        self, ctx: commands.Context, react: bool = False, *, action: str = None
    ) -> None:
        if react:
            await ctx.message.add_reaction("✅")
        else:
            embed = lucid_embed(ctx, success=True).set_author(
                name=f"Successfully {action}",
                icon_url="https://i.imgur.com/4yUeOVj.gif",
            )
            await ctx.send(embed=embed)

    async def yes_no_dialogue(
        self,
        message: discord.Message,
        ctx: commands.Context,
        timeout: int = 20,
        dm: bool = False,
    ) -> bool:
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        while True:

            try:
                reaction = await self.bot.wait_for("reaction_add", timeout=timeout)

            except asyncio.TimeoutError:
                embed = lucid_embed(
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

    async def announcement_channel(
        self, ctx: commands.Context, message: discord.Message
    ):
        # EMBED CHANNEL
        while True:

            try:
                announce_channel_message: discord.Message = await self.bot.wait_for(
                    "message", timeout=20
                )

            except asyncio.TimeoutError:
                embed = lucid_embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )
                await message.edit(embed=embed)

                return None

            if announce_channel_message.author.id == ctx.author.id:
                await announce_channel_message.delete()
                channel_tag: str = announce_channel_message.content

                try:
                    announce_channel: discord.abc.GuildChannel = (
                        announce_channel_message.channel_mentions[0]
                    )

                except IndexError:
                    embed = lucid_embed(
                        title="Command Error -",
                        description="Did you mention a valid channel?",
                    )
                    await message.edit(embed=embed)

                    return None

                break

        return announce_channel, channel_tag

    async def announce_title(
        self, ctx: commands.Context, message: discord.Message
    ) -> str:
        # EMBED TITLE
        embed = lucid_embed(
            title="Bot Announcement -",
            description="What should the title of the announcement be?",
        )

        await message.edit(embed=embed)

        while True:

            try:
                announce_title_message: discord.Message = await self.bot.wait_for(
                    "message", timeout=60
                )

            except asyncio.TimeoutError:
                embed = lucid_embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )

                await message.edit(embed=embed)

                return None

            if announce_title_message.author.id == ctx.author.id:
                await announce_title_message.delete()

                break

        return announce_title_message.content

    async def announcement_description(
        self, ctx: commands.Context, message: discord.Message
    ) -> str:
        # EMBED DESCRIPTION
        embed = lucid_embed(
            title="Bot Announcement -",
            description="What should the announcement say?",
        )

        await message.edit(embed=embed)

        while True:

            try:
                announce_description_message: discord.Message = await self.bot.wait_for(
                    "message", timeout=180
                )

            except asyncio.TimeoutError:
                embed = lucid_embed(
                    title="Timeout",
                    description="Sorry, you took too long to respond.",
                )

                await message.edit(embed=embed)

                return None

            if announce_description_message.author.id == ctx.author.id:
                await announce_description_message.delete()

                break

        return announce_description_message.content

    async def announce_color(
        self, message: discord.Message, ctx: commands.Context
    ) -> str:
        embed = lucid_embed(
            title="Bot Announcement -",
            description="What should the color of the embed be?\n\n(Wait for all reactions to "
            "appear.)",
        )

        await message.edit(embed=embed)

        for value in self.config["reactColors"]:
            await message.add_reaction(self.config["reactColors"][value])

        while True:

            try:
                reactColor = await self.bot.wait_for("reaction_add", timeout=20)

            except asyncio.TimeoutError:
                embed = lucid_embed(
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
        self,
        ctx: commands.Context,
        announce_channel: discord.abc.GuildChannel,
        announce_embed: discord.Embed,
        channel_tag: str,
    ) -> None:
        # CONFIRM/DENY SEND
        embed = lucid_embed(
            title="Bot Announcement -",
            description="Do you want to send the announcement " + "as shown above?",
        )
        message: discord.Message = await ctx.send(embed=embed)

        reaction_yes: bool = await self.yes_no_dialogue(message, ctx, 10, False)

        if reaction_yes:
            await announce_channel.send(embed=announce_embed)
            embed = lucid_embed(
                title="Bot Announcement -",
                description="Announcement successfully sent to " + channel_tag + ".",
            )
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)

        else:
            embed = lucid_embed(
                title="Bot Announcement -",
                description="Announcement Cancelled.",
            )
            embed.set_footer(text="bot developed by viargentum#3850")
            await message.clear_reactions()
            await message.edit(embed=embed)

        return
