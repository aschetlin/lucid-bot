from lucid_bot.bot import bot
from lucid_bot.config import config
import lucid_bot.commands # noqa
from lucid_bot.commands import moderation # noqa

bot.run(config["token"])
