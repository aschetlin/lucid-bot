import random

from discord.ext import commands

from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config

    @commands.command(name="help")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _help(self, ctx, *args):
        prefix = self.config["prefix"]
        hexInt = int(random.choice(list(self.config["colors"])), 16)
        botName = self.config["botName"]

        if not args:
            embed = lucid_embed(
                title=f"{botName} Bot Help -",
                color=hexInt,
                description=f"use {prefix}help <category> "
                f"to get more info",
            )
            embed.add_field(
                name="Utility -",
                value="`ping`, `help`, `info`",
                inline=False,
            )
            embed.add_field(
                name="General -",
                value="`report`, `announce`, `say`",
                inline=False,
            )
            embed.add_field(
                name="Moderation -",
                value="`kick`, `mute`, `unmute`, `ban`, `unban`, `slowmode`, `lockdown (wip)`",
                inline=False,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "utility":
            embed = lucid_embed(
                title="Utility Commands Help -",
                color=hexInt,
                description="\n\n".join(config["utilities"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "general":
            embed = lucid_embed(
                title="General Commands Help -",
                color=hexInt,
                description="\n\n".join(config["general"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        elif args[0].lower() == "moderation":
            embed = lucid_embed(
                title="Moderation Commands Help -",
                color=hexInt,
                description="\n\n".join(config["moderation"]),
                inline=True,
            )

            await ctx.send(embed=embed)

        else:
            embed = lucid_embed(
                title="Unknown Help Category -",
                description=f"{args[0]} is not a category.",
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
