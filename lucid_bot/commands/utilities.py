import discord
import random
from lucid_bot.config import config
from lucid_bot.bot import bot


@bot.command(aliases=["ms", "delay"])
async def ping(ctx):
    pingMsg = await ctx.send("*pinging...*")
    msgPing = round((pingMsg.created_at - ctx.message.created_at).total_seconds() * 1000)

    await pingMsg.delete()
    botPing = round(bot.latency * 1000)
    hexInt = int(random.choice(list(config["colors"])), 16)

    embed = discord.Embed(title="Ping -", color=hexInt)
    embed.add_field(name=f"API Latency", value=f"~{botPing}ms")
    embed.add_field(name=f"Message Latency", value=f"~{msgPing}ms")

    await ctx.send(embed=embed)
