import random

import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(aliases=["ms", "delay"])
    async def ping(self, ctx):
        pingMsg = await ctx.send("*pinging...*")
        msgPing = round(
            (pingMsg.created_at - ctx.message.created_at).total_seconds()
            * 1000
        )

        await pingMsg.delete()
        botPing = round(self.bot.latency * 1000)
        hexInt = int(random.choice(list(self.config["colors"])), 16)

        embed = discord.Embed(title="Ping -", color=hexInt)
        embed.add_field(name=f"API Latency:", value=f"~{botPing}ms")
        embed.add_field(name=f"Message Latency:", value=f"~{msgPing}ms")

        await ctx.send(embed=embed)
