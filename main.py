#!/usr/bin/env python3

import discord
from discord.ext import commands

from lucid_bot import cog_config, non_bot_funcs
from lucid_bot.config import config

# Bot init
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=config["prefix"], case_insensitive=False, intents=intents
)
bot.remove_command("help")

# non_bot_funcs init
nbf = non_bot_funcs.NonBotFuncs(bot, config)

# Adding cogs (may be a better way of doing this)
for cog in cog_config.cogs:
    optional_params = []

    if cog.get("config"):
        optional_params.append(config)
    if cog.get("nbf"):
        optional_params.append(nbf)

    current_class = cog["class"]
    print(f"Loading {current_class.__name__}....")

    bot.add_cog(cog["class"](bot, *optional_params))

# Run da bot
bot.run(config["token"])
