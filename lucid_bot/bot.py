import discord
from discord.ext import commands
from lucid_bot.config import config


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=False, intents=intents)


@bot.event
async def on_ready():
    print(config["botName"] + " " + "bot online\n---")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Command Error -", description="Command not found.")
        await ctx.send(embed=embed)

    else:
        raise error
