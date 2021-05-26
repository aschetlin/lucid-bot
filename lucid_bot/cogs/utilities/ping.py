import random

from discord.ext import commands

from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config

    @commands.command(name="ping", aliases=["ms", "delay"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _ping(self, ctx):
        pingMsg = await ctx.send("*pinging...*")
        msgPing = round(
            (pingMsg.created_at - ctx.message.created_at).total_seconds()
            * 1000
        )

        await pingMsg.delete()
        botPing = round(self.bot.latency * 1000)
        hexInt = int(random.choice(list(self.config["colors"])), 16)

        embed = lucid_embed(title="Ping -", color=hexInt)
        embed.add_field(name=f"API Latency:", value=f"~{botPing}ms")
        embed.add_field(name=f"Message Latency:", value=f"~{msgPing}ms")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
