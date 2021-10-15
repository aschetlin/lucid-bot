#!/usr/bin/env python

import discord
from discord.ext import commands

from lucid_bot.config import config
from lucid_bot.utils import Utils
from lucid_bot.extension_config import extensions

intents: discord.Intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=config["prefix"],
    case_insensitive=False,
    intents=intents,
)
bot.remove_command("help")

for extension in extensions:
    optional_params = []
    current_extension = extensions[extension]
    time = Utils.time()
    print(f"{time}Loading {extension.capitalize()}....")

    bot.load_extension(current_extension)


bot.run(config["token"])
