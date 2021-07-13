from discord.ext import commands

from lucid_bot.extension_config import extensions
from lucid_bot.utils import Utils, LucidCommandResult


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utils = Utils

    @commands.group(name="reload", hidden=True, invoke_without_command=True)
    @commands.is_owner()
    async def _reload(self, ctx: commands.Context, module: str) -> None:
        try:
            self.bot.reload_extension(extensions[module])
            await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)

        except commands.ExtensionError as e:
            print(e)
            await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)

    @_reload.command(name="all", hidden=True)
    async def _reload_all(self, ctx: commands.Context) -> None:
        try:
            for extension in extensions:
                self.bot.reload_extension(extensions[extension])

            await self.utils.command_result(ctx, result=LucidCommandResult.SUCCESS)

        except commands.ExtensionError as e:
            print(e)
            await self.utils.command_result(ctx, result=LucidCommandResult.FAIL)


def setup(bot):
    bot.add_cog(Reload(bot))
