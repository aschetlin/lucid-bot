#!/usr/bin/env python

import discord
from discord.ext import commands

from lucid_bot import extension_config
from lucid_bot.cogs.moderation import ban
from lucid_bot.config import config
from lucid_bot.utils import Utils

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=config["prefix"], case_insensitive=False, intents=intents
)
bot.remove_command("help")


for extension in extension_config.extension:
    optional_params = []
    current_extension = extension_config.extension[extension]
    time = Utils.time()
    print(f"{time}Loading {extension.capitalize()}....")

    bot.load_extension(current_extension)


bot.run(config["token"])
