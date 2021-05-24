import json
from discord.ext import commands
from lucid_bot import config


class Repost(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = config.config

    @commands.command(name="repost")
    @commands.has_permissions(administrator=True)
    async def _repost(self, ctx, *args):
        if args[0] == "activate":
            with open("./config.json", "r+") as file:
                json_object = json.load(file)
                json_object["reposter"]["active"] = True
                file.seek(0)
                json.dump(json_object, file)
                file.truncate()

            await ctx.message.add_reaction("✅")

        elif args[0] == "deactivate":
            with open("./config.json", "r+") as file:
                json_object = json.load(file)
                json_object["reposter"]["active"] = False
                file.seek(0)
                json.dump(json_object, file)
                file.truncate()

            await ctx.message.add_reaction("✅")

        elif args[0] == "user":
            with open("./config.json", "r+") as file:
                json_object = json.load(file)
                json_object["reposter"]["targetUserId"] = int(args[1])
                file.seek(0)
                json.dump(json_object, file)
                file.truncate()

            await ctx.message.add_reaction("✅")

        elif args[0] == "channel":
            with open("./config.json", "r+") as file:
                json_object = json.load(file)
                json_object["reposter"]["targetChannelId"] = int(args[1])
                file.seek(0)
                json.dump(json_object, file)
                file.truncate()

            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Repost(bot))
