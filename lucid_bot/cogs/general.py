import discord
from discord.ext import commands
import asyncio
import redis


class General(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf
        self.r = redis.Redis(host=self.config["redis"]["hostname"], port=self.config["redis"]["port"], db=self.config["redis"]["db"])

    @commands.command(aliases=["issue"])
    async def report(self, ctx):
        embed = discord.Embed(title="Issue Report -", description="Issue report started in your dms!")
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Issue Report -", description="Would you like to start an issue report ticket?")
        message = await ctx.author.send(embed=embed)

        startTicket = await self.nbf.yes_no_dialogue(message, 30, True, ctx)

        if startTicket:

            embed = discord.Embed(title="Issue Report -", description="What should the title of your issue be?")
            await ctx.author.send(embed=embed)

            while True:

                try:
                    issueTitle = await self.bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to respond.")
                    await ctx.author.send(embed=embed)

                    return None

                if issueTitle.author.id == ctx.author.id:
                    break

            while True:

                embed = discord.Embed(title="Issue Report -", description="Describe your issue as detailed as possible, "
                                                                        "and how to recreate it, (if applicable).")
                await ctx.author.send(embed=embed)

                try:
                    issueDescription = await self.bot.wait_for("message", timeout=120)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to respond.")
                    await ctx.author.send(embed=embed)

                    return None

                if issueDescription.author.id == ctx.author.id:
                    embed = discord.Embed(title="Issue Report -", description="Issue report successfully filed, thank you!",
                                        color=0x00fe5f)
                    await ctx.author.send(embed=embed)

                    user = self.bot.get_user(581593263736356885)
                    ticketcount = int(self.r.get("ticketcount") or 0)

                    await user.send(f"**Issue Ticket #{ticketcount} - **")

                    embed = discord.Embed(title=str(issueTitle.content), description=str(issueDescription.content))
                    embed.set_footer(text=str(ctx.author) + " - " + str(ctx.author.id))

                    await user.send(embed=embed)

                    r.set("ticketcount", int(ticketcount) + 1)

                    break

        else:
            embed = discord.Embed(title="Issue Report -", description="Ticket creation cancelled.")
            await ctx.author.send(embed=embed)


    @commands.command(aliases=["announcement"])
    async def announce(self, ctx, *args):
        if ctx.author.guild_permissions.administrator or ctx.author.id in self.config["adminIDS"]:

            if not args:
                embed = discord.Embed(
                    title="Bot Announcement -", description="What channel should the announcement be sent to?")

                message = await ctx.send(embed=embed)

                announceChannel, channelTag = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)
                announceMessage = await self.nbf.announcement_description(ctx, message)
                colorHex = await self.nbf.announce_color(message, ctx)

                # ANNOUNCEMENT AUTHOR YES/NO

                embed = discord.Embed(title="Should the announcement list who created it in the footer,\n"
                                            "eg. the footer of this message?")
                embed.set_footer(text="announcement from " + str(ctx.author))

                await message.clear_reactions()

                await message.edit(embed=embed)

                reaction_yes = await self.nbf.yes_no_dialogue(message, 10, False, ctx)

                # BUILDING ANNOUNCEMENT EMBED
                hexInt = int(colorHex, 16)
                announceEmbed = discord.Embed(title=announceTitle, description=announceMessage,
                                            color=hexInt)

                if reaction_yes:
                    announceEmbed.set_footer(text="announcement from " + str(ctx.author))

                await message.clear_reactions()

                await message.edit(embed=announceEmbed)

                await self.nbf.announcement_send(ctx, announceChannel, announceEmbed, channelTag)

            elif args[0].lower() == "image":
                embed = discord.Embed(
                    title="Bot Announcement -", description="What channel should the announcement be sent to?")

                message = await ctx.send(embed=embed)

                announceChannel, channelTag = await self.nbf.announcement_channel(ctx, message)
                announceTitle = await self.nbf.announce_title(ctx, message)

                embed = discord.Embed(title="Bot Announcement -", description="Should the embed have a description?")
                await message.edit(embed=embed)
                embedDescription = await self.nbf.yes_no_dialogue(message, 20, False, ctx)

                if embedDescription:
                    announceMessage = await self.nbf.announcement_description(ctx, message)

                else:
                    announceMessage = ""

                embed = discord.Embed(title="Bot Announcement -", description="Please link the image url.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                while True:

                    try:
                        image = await self.bot.wait_for("message", timeout=40)

                    except asyncio.TimeoutError:
                        embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to respond.")
                        await message.edit(embed=embed)

                        return None

                    if image.author.id == ctx.author.id:
                        break

                colorHex = await self.nbf.announce_color(message, ctx)
                hexInt = int(colorHex, 16)

                if embedDescription:
                    announceEmbed = discord.Embed(title=announceTitle, description=announceMessage, color=hexInt)

                else:
                    announceEmbed = discord.Embed(title=announceTitle)

                announceEmbed.set_image(url=image.content)

                await ctx.send(embed=announceEmbed)

                await self.nbf.announcement_send(ctx, announceChannel, announceEmbed, channelTag)

        else:
            embed = discord.Embed(title="Permissions Error -", description="Sorry, you don't have the required "
                                                                        "permissions to execute that command.")
            await ctx.send(embed=embed)


    @commands.command()
    async def say(self, ctx, *, message):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            await ctx.send(message)

        else:
            embed = discord.Embed(title="Permissions Error -", description="Sorry, you don't have the required "
                                                                        "permissions to execute that command.")
            await ctx.send(embed=embed)
