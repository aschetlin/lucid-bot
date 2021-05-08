#!/usr/bin/env python3

import discord
from discord.ext import commands

from lucid_bot import extension_config, non_bot_funcs
from lucid_bot.cogs.moderation import ban
from lucid_bot.config import config

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=config["prefix"], case_insensitive=False, intents=intents
)
bot.remove_command("help")

# nbf = non_bot_funcs.NonBotFuncs(bot, config)


for extension in extension_config.extension:
    optional_params = []
    current_extension = extension_config.extension[extension]
    print(f"Loading {extension.capitalize()}....")

    bot.load_extension(current_extension)


bot.run(config["token"])
