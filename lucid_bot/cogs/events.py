from discord.ext import commands
from lucid_bot import config, utils
from lucid_bot.lucid_embed import lucid_embed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
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
            f"{time}{ctx.author} | {ctx.author.id} did `{ctx.message.content}`"
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            embed = lucid_embed(
                title="Command Error -", description="Command not found."
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = lucid_embed(
                title="Permissions Error -",
                description="You don't have the required permissions to "
                "execute that command.",
            )
            await ctx.send(embed=embed)

        else:
            raise error


def setup(bot):
    bot.add_cog(Events(bot))
