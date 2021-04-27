import random

import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command()
    async def info(self, ctx):
        prefix = self.config["prefix"]
        botName = self.config["botName"]
        hexInt = int(random.choice(list(self.config["colors"])), 16)

        embed = discord.Embed(title=f"{botName} Bot Info", color=hexInt)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Built by:", value="viargentum#3850", inline=False
        )
        embed.add_field(
            name="Issues or suggestions:",
            value=f"If you have any issues or suggestions, use {prefix}report or"
            f" create an issue on "
            f"https://www.github.com/viargentum/lucid-bot",
            inline=False,
        )

        await ctx.send(embed=embed)
