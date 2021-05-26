from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_permissions(manage_channels=True)
    async def _say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Say(bot))
