#!/usr/bin/env python3

import discord
from discord.ext import commands

import lucid_bot
from lucid_bot import non_bot_funcs
from lucid_bot.config import config
from lucid_bot.cogs import events, general, moderation, utilities


# Bot init
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=False, intents=intents)
bot.remove_command("help")

# non_bot_funcs init
nbf = non_bot_funcs.NonBotFuncs(bot, config)

# Adding cogs (may be a better way of doing this)
bot.add_cog(events.Events(bot, config))
bot.add_cog(general.General(bot, config, nbf))
bot.add_cog(moderation.Moderation(bot, config, nbf))
bot.add_cog(utilities.Utilities(bot, config))

# Run da bot
bot.run(config["token"])