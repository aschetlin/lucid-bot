from discord.ext import commands
from lucid_bot.embed import Embed


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

        embed = Embed(
            ctx,
            success=True,
            title="Message Purge -",
            description=f"Successfully purged {amount} messages.",
            icon_url="https://i.imgur.com/4yUeOVj.gif",
        )
        await ctx.send(embed=embed)
