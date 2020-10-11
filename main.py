from lucid_bot.bot import bot
from lucid_bot.config import config
import lucid_bot.commands
from lucid_bot.commands import moderation

bot.run(config["token"])
