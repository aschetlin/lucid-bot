#!/usr/bin/env python3

from lucid_bot.bot import bot, slash
from lucid_bot.config import config
import lucid_bot.commands # noqa
from lucid_bot.commands import moderation, utilities # noqa


bot.run(config["token"])
