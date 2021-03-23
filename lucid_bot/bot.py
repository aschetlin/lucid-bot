import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from lucid_bot.config import config

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=False, intents=intents)
slash = SlashCommand(bot, sync_commands=True) # declaring slash commands
guild_ids = [387368495979036672, 704559844916723723]
bot.remove_command("help")


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
