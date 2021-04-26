from datetime import datetime

import discord
from discord.colour import Color


def Embed(ctx=None, success: bool = None, **kwargs):
    if success:
        kwargs["color"] = Color.green()

    elif success is False:
        kwargs["color"] = Color.red()

    embed = discord.Embed(**kwargs, timestamp=datetime.utcnow())

    if ctx:
        embed.set_footer(text=ctx.author)

    return embed
