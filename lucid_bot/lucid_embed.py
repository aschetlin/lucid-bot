from datetime import datetime

import discord
from discord.colour import Color
from discord.ext import commands


def lucid_embed(
    ctx: commands.Context = None, success: bool = None, fail: bool = None, **kwargs
) -> discord.Embed:
    if success:
        kwargs["color"] = Color.green()

    elif fail:
        kwargs["color"] = Color.red()

    else:
        kwargs["color"] = int("2F3136", 16)

    embed = discord.Embed(**kwargs, timestamp=datetime.utcnow())

    if ctx:
        embed.set_footer(text=ctx.author)

    return embed
