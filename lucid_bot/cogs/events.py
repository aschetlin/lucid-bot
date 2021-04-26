import discord
from discord.ext import commands
from lucid_bot.non_bot_funcs import NonBotFuncs


class Events(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.config["botName"] + " " + "bot online\n---")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Error -", description="Command not found."
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Permissions Error -",
                description="You don't have the required permissions to "
                "execute that command.",
            )
            await ctx.send(embed=embed)

        else:
            raise error
