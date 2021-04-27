import asyncio

import discord
import redis
from discord.ext import commands


class Report(commands.Cog):
    def __init__(self, bot, config, nbf):
        self.bot = bot
        self.config = config
        self.nbf = nbf
        self.r = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
        )

    @commands.command(aliases=["issue"])
    async def report(self, ctx):
        embed = discord.Embed(
            title="Issue Report -",
            description="Issue report started in your dms!",
        )
        await ctx.send(embed=embed)

        embed = discord.Embed(
            title="Issue Report -",
            description="Would you like to start an issue report ticket?",
        )
        message = await ctx.author.send(embed=embed)

        startTicket = await self.nbf.yes_no_dialogue(message, 30, True, ctx)

        if startTicket:

            embed = discord.Embed(
                title="Issue Report -",
                description="What should the title of your issue be?",
            )
            await ctx.author.send(embed=embed)

            while True:

                try:
                    issueTitle = await self.bot.wait_for(
                        "message", timeout=20
                    )

                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await ctx.author.send(embed=embed)

                    return None

                if issueTitle.author.id == ctx.author.id:
                    break

            while True:

                embed = discord.Embed(
                    title="Issue Report -",
                    description="Describe your issue as detailed as possible, "
                    "and how to recreate it, (if applicable).",
                )
                await ctx.author.send(embed=embed)

                try:
                    issueDescription = await self.bot.wait_for(
                        "message", timeout=120
                    )

                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await ctx.author.send(embed=embed)

                    return None

                if issueDescription.author.id == ctx.author.id:
                    embed = discord.Embed(
                        title="Issue Report -",
                        description="Issue report successfully filed, thank you!",
                        color=0x00FE5F,
                    )
                    await ctx.author.send(embed=embed)

                    user = self.bot.get_user(581593263736356885)
                    ticketcount = int(self.r.get("ticketcount") or 0)

                    await user.send(f"**Issue Ticket #{ticketcount} - **")

                    embed = discord.Embed(
                        title=str(issueTitle.content),
                        description=str(issueDescription.content),
                    )
                    embed.set_footer(
                        text=str(ctx.author) + " - " + str(ctx.author.id)
                    )

                    await user.send(embed=embed)

                    r.set("ticketcount", int(ticketcount) + 1)

                    break

        else:
            embed = discord.Embed(
                title="Issue Report -",
                description="Ticket creation cancelled.",
            )
            await ctx.author.send(embed=embed)
