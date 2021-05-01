import random

import discord
from discord.ext import commands
from lucid_bot.embed import embed


class Help(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command()
    async def help(self, ctx, *args):
        prefix = self.config["prefix"]
        hexInt = int(random.choice(list(self.config["colors"])), 16)
        botName = self.config["botName"]

        if not args:
            embed = embed(
                title=f"{botName} Bot Help -",
                color=hexInt,
                description=f"use {prefix}help <category> " f"to get more info",
            )
            embed.add_field(
                name="Utility -",
                value="`ping`, `help`, `info`",
                inline=False,
            )
            embed.add_field(
                name="General -", value="`report`, `announce`, `say`", inline=False
            )
            embed.add_field(
                name="Moderation -",
                value="`kick`, `mute`, `unmute`, `ban`, `unban`, `slowmode`, `lockdown (wip)`",
                inline=False,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "utility":
            embed = embed(
                title="Utility Commands Help -",
                color=hexInt,
                description="\n\n".join(self.config["utilities"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "general":
            embed = embed(
                title="General Commands Help -",
                color=hexInt,
                description="\n\n".join(self.config["general"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "moderation":
            embed = embed(
                title="Moderation Commands Help -",
                color=hexInt,
                description="\n\n".join(self.config["moderation"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        else:
            embed = embed(
                title="Unknown Help Category -",
                description=f"{args[0]} is not a category.",
            )
            await ctx.send(embed=embed)
