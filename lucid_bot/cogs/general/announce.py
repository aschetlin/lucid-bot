import asyncio

from discord.ext import commands

from lucid_bot import config, utils
from lucid_bot.lucid_embed import lucid_embed


class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
        self.nbf = utils.Utils(bot)

    @commands.command(name="announce", aliases=["announcement"])
    @commands.has_permissions(manage_guild=True)
    async def _announce(self, ctx: commands.Context, *args) -> None:
        if (
            ctx.author.guild_permissions.administrator
            or ctx.author.id in self.config["adminIDS"]
        ):

            if not args:
                embed = lucid_embed(
                    title="Bot Announcement -",
                    description="What channel should the announcement be sent to?",
                )

                message = await ctx.send(embed=embed)
                (
                    announceChannel,
                    channelTag,
                ) = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)
                announceMessage = await self.nbf.announcement_description(ctx, message)
                colorHex = await self.nbf.announce_color(message, ctx)

                # ANNOUNCEMENT AUTHOR YES/NO

                embed = lucid_embed(
                    title="Should the announcement list who created it in the footer,\n"
                    "eg. the footer of this message?"
                )
                embed.set_footer(text="announcement from " + str(ctx.author))

                await message.clear_reactions()

                await message.edit(embed=embed)

                reaction_yes = await self.nbf.yes_no_dialogue(message, ctx, 10, False)

                # BUILDING ANNOUNCEMENT EMBED
                hexInt = int(colorHex, 16)
                announceEmbed = lucid_embed(
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
                embed = lucid_embed(
                    title="Bot Announcement -",
                    description="What channel should the announcement be sent to?",
                )

                message = await ctx.send(embed=embed)

                (
                    announceChannel,
                    channelTag,
                ) = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)

                embed = lucid_embed(
                    title="Bot Announcement -",
                    description="Should the embed have a description?",
                )
                await message.edit(embed=embed)
                embedDescription = await self.nbf.yes_no_dialogue(
                    message, ctx, 20, False
                )

                if embedDescription:
                    announceMessage = await self.nbf.announcement_description(
                        ctx, message
                    )

                else:
                    announceMessage = ""

                embed = lucid_embed(
                    title="Bot Announcement -",
                    description="Please link the image url.",
                )
                await message.clear_reactions()
                await message.edit(embed=embed)

                while True:

                    try:
                        image = await self.bot.wait_for("message", timeout=40)

                    except asyncio.TimeoutError:
                        embed = lucid_embed(
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
                    announceEmbed = lucid_embed(
                        title=announceTitle,
                        description=announceMessage,
                        color=hexInt,
                    )

                else:
                    announceEmbed = lucid_embed(title=announceTitle)

                announceEmbed.set_image(url=image.content)

                await ctx.send(embed=announceEmbed)

                await self.nbf.announcement_send(
                    ctx, announceChannel, announceEmbed, channelTag
                )

        else:
            embed = lucid_embed(
                title="Permissions Error -",
                description="Sorry, you don't have the required "
                "permissions to execute that command.",
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Announce(bot))
