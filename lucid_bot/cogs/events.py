import redis
from discord.ext import commands
from lucid_bot import config, utils


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
        self.redis = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
            decode_responses=True,
        )
        self.utils = utils.Utils

    @commands.Cog.listener()
    async def on_connect(self):
        time = self.utils.time()
        print(f"\n{time}Bot connected to Discord.")

    @commands.Cog.listener()
    async def on_ready(self):
        botName = self.config["botName"]
        time = self.utils.time()
        print(f"\n{time}{botName} Bot ready.")
        print("-----------------------------")

    @commands.Cog.listener()
    async def on_disconnect(self):
        time = self.utils.time()
        print("-----------------------------")
        print(f"\n{time}Bot disconnected.")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        time = self.utils.time()
        print(
            f"{time}{ctx.author}::{ctx.author.id} did `{ctx.message.content}`"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        repost_active = self.redis.hget(message.guild.id, "repostActive")

        if repost_active == "True":
            target_user = self.redis.hget(
                message.guild.id, "repostTargetUser"
            )

            if message.author.id == int(target_user):
                print(f"here {message.author.id}")

                await message.delete()

                channel_id = self.redis.hget(
                    message.guild.id, "repostTargetChannel"
                )
                channel = self.bot.get_channel(int(channel_id))
                await channel.send(message.content)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("❓")

        elif isinstance(error, commands.CheckFailure):
            await ctx.message.add_reaction("❌")

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("🕐")

        else:
            raise error


def setup(bot):
    bot.add_cog(Events(bot))
