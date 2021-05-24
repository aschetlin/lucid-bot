import asyncio

import redis
from discord.ext import commands
from lucid_bot import config, utils
from lucid_bot.lucid_embed import lucid_embed


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
        self.nbf = utils.Utils(bot)
        self.r = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
        )

    @commands.command(name="report", aliases=["issue"])
    @commands.is_owner()
    async def _report(self, ctx):
        embed = lucid_embed(
            title="Issue Report -",
            description="Issue report started in your dms!",
        )
        await ctx.send(embed=embed)

        embed = lucid_embed(
            title="Issue Report -",
            description="Would you like to start an issue report ticket?",
        )
        message = await ctx.author.send(embed=embed)
        startTicket = await self.nbf.yes_no_dialogue(message, ctx, 30, True)

        if startTicket:

            embed = lucid_embed(
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
                    embed = lucid_embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await ctx.author.send(embed=embed)

                    return None

                if issueTitle.author.id == ctx.author.id:
                    break

            while True:

                embed = lucid_embed(
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
                    embed = lucid_embed(
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await ctx.author.send(embed=embed)

                    return None

                if issueDescription.author.id == ctx.author.id:
                    embed = lucid_embed(
                        title="Issue Report -",
                        description="Issue report successfully filed, thank you!",
                        color=0x00FE5F,
                    )
                    await ctx.author.send(embed=embed)

                    user = self.bot.get_user(581593263736356885)
                    ticketcount = int(self.r.get("ticketcount") or 0)

                    await user.send(f"**Issue Ticket #{ticketcount} - **")

                    embed = lucid_embed(
                        title=str(issueTitle.content),
                        description=str(issueDescription.content),
                    )
                    embed.set_footer(
                        text=str(ctx.author) + " - " + str(ctx.author.id)
                    )

                    await user.send(embed=embed)

                    self.r.set("ticketcount", int(ticketcount) + 1)

                    break

        else:
            embed = lucid_embed(
                title="Issue Report -",
                description="Ticket creation cancelled.",
            )
            await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Report(bot))
