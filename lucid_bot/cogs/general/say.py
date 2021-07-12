from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def _say(self, ctx: commands.Context, *, message: str) -> None:
        await ctx.message.delete()
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Say(bot))
