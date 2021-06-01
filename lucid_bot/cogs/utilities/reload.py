from discord.ext import commands

from lucid_bot.extension_config import extension


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, module):
        try:
            self.bot.reload_extension(
                extension[module], package="lucid_bot.cogs"
            )

        except commands.ExtensionError as e:
            print(e)
            await ctx.message.add_reaction("❌")

        else:
            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Reload(bot))
