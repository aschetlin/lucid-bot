import asyncio

import discord
from discord.ext import commands
from lucid_bot.embed import embed


class Announce(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf

    @commands.command(aliases=["announcement"])
    async def announce(self, ctx, *args):
        if (
            ctx.author.guild_permissions.administrator
            or ctx.author.id in self.config["adminIDS"]
        ):

            if not args:
                embed = embed(
                    title="Bot Announcement -",
                    description="What channel should the announcement be sent to?",
                )

                message = await ctx.send(embed=embed)

                (
                    announceChannel,
                    channelTag,
                ) = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)
                announceMessage = await self.nbf.announcement_description(
                    ctx, message
                )
                colorHex = await self.nbf.announce_color(message, ctx)

                # ANNOUNCEMENT AUTHOR YES/NO

                embed = embed(
                    title="Should the announcement list who created it in the footer,\n"
                    "eg. the footer of this message?"
                )
                embed.set_footer(text="announcement from " + str(ctx.author))

                await message.clear_reactions()

                await message.edit(embed=embed)

                reaction_yes = await self.nbf.yes_no_dialogue(
                    message, 10, False, ctx
                )

                # BUILDING ANNOUNCEMENT EMBED
                hexInt = int(colorHex, 16)
                announceEmbed = embed(
                    title=announceTitle,
                    description=announceMessage,
                    color=hexInt,
                )

                if reaction_yes:
                    announceEmbed.set_footer(
                        text="announcement from " + str(ctx.author)
                    )

                await message.clear_reactions()

                await message.edit(embed=announceEmbed)

                await self.nbf.announcement_send(
                    ctx, announceChannel, announceEmbed, channelTag
                )

            elif args[0].lower() == "image":
                embed = embed(
                    title="Bot Announcement -",
                    description="What channel should the announcement be sent to?",
                )

                message = await ctx.send(embed=embed)

                (
                    announceChannel,
                    channelTag,
                ) = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)

                embed = embed(
                    title="Bot Announcement -",
                    description="Should the embed have a description?",
                )
                await message.edit(embed=embed)
                embedDescription = await self.nbf.yes_no_dialogue(
                    message, 20, False, ctx
                )

                if embedDescription:
                    announceMessage = await self.nbf.announcement_description(
                        ctx, message
                    )

                else:
                    announceMessage = ""

                embed = embed(
                    title="Bot Announcement -",
                    description="Please link the image url.",
                )
                await message.clear_reactions()
                await message.edit(embed=embed)

                while True:

                    try:
                        image = await self.bot.wait_for("message", timeout=40)

                    except asyncio.TimeoutError:
                        embed = embed(
                            title="Timeout -",
                            description="Sorry, you took too long to respond.",
                        )
                        await message.edit(embed=embed)

                        return None

                    if image.author.id == ctx.author.id:
                        break

                colorHex = await self.nbf.announce_color(message, ctx)
                hexInt = int(colorHex, 16)

                if embedDescription:
                    announceEmbed = embed(
                        title=announceTitle,
                        description=announceMessage,
                        color=hexInt,
                    )

                else:
                    announceEmbed = embed(title=announceTitle)

                announceEmbed.set_image(url=image.content)

                await ctx.send(embed=announceEmbed)

                await self.nbf.announcement_send(
                    ctx, announceChannel, announceEmbed, channelTag
                )

        else:
            embed = embed(
                title="Permissions Error -",
                description="Sorry, you don't have the required "
                "permissions to execute that command.",
            )
            await ctx.send(embed=embed)
