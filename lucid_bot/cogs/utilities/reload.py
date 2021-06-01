from discord.ext import commands

from lucid_bot.extension_config import extensions


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    @commands.is_owner()
    async def _reload(self, ctx, module):
        try:
            self.bot.reload_extension(extensions[module])
            await ctx.message.add_reaction("✅")

        except commands.ExtensionError as e:
            print(e)
            await ctx.message.add_reaction("❌")

    @_reload.command(name="all", hidden=True)
    async def _reload_all(self, ctx):
        try:
            for extension in extensions:
                self.bot.reload_extension(extensions[extension])

            await ctx.message.add_reaction("✅")

        except commands.ExtensionError as e:
            print(e)
            await ctx.message.add_reaction("❌")


def setup(bot):
    bot.add_cog(Reload(bot))
