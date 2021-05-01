from datetime import datetime

import discord
from discord.colour import Color


def embed(ctx=None, success: bool = None, **kwargs):
    if success:
        kwargs["color"] = Color.green()

    elif success is False:
        kwargs["color"] = Color.red()

    embed = embed(**kwargs, timestamp=datetime.utcnow())

    if ctx:
        embed.set_footer(text=ctx.author)

    return embed
