import discord
from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            await ctx.send(message)

        else:
            embed = discord.Embed(
                title="Permissions Error -",
                description="Sorry, you don't have the required "
                "permissions to execute that command.",
            )
            await ctx.send(embed=embed)
