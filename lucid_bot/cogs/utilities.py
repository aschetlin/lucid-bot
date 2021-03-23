import discord
from discord.ext import commands
import random


class Utilities(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(aliases=["ms", "delay"])
    async def ping(self, ctx):
        pingMsg = await ctx.send("*pinging...*")
        msgPing = round((pingMsg.created_at - ctx.message.created_at).total_seconds() * 1000)

        await pingMsg.delete()
        botPing = round(self.bot.latency * 1000)
        hexInt = int(random.choice(list(self.config["colors"])), 16)

        embed = discord.Embed(title="Ping -", color=hexInt)
        embed.add_field(name=f"API Latency:", value=f"~{botPing}ms")
        embed.add_field(name=f"Message Latency:", value=f"~{msgPing}ms")

        await ctx.send(embed=embed)


    @commands.command()
    async def help(self, ctx, *args): # maybe we make this a bit better later, i think cogs can be used to help it along
        prefix = self.config["prefix"]
        hexInt = int(random.choice(list(self.config["colors"])), 16)
        botName = self.config["botName"]

        if not args:
            embed = discord.Embed(title=f"{botName} Bot Help -", color=hexInt, description=f"use {prefix}help <category> "
                                                                                        f"to get more info")
            embed.add_field(name="Utility -", value="`ping`, `help`, `info`, `purchase`", inline=False)
            embed.add_field(name="General -", value="`report`, `announce`, `say`", inline=False)
            embed.add_field(name="Moderation -", value="`kick`, `mute`, `ban`, `slowmode`, `lockdown`", inline=False)

            await ctx.send(embed=embed)

        elif args[0].lower() == "utility":
            embed = discord.Embed(title="Utility Commands Help -", color=hexInt, description="\n\n".join(
                self.config["commandList"]["utilities"]), inline=True)

            await ctx.send(embed=embed)

        elif args[0].lower() == "general":
            embed = discord.Embed(title="General Commands Help -", color=hexInt, description="\n\n".join(
                self.config["commandList"]["general"]), inline=True)

            await ctx.send(embed=embed)

        elif args[0].lower() == "moderation":
            embed = discord.Embed(title="Moderation Commands Help -", color=hexInt, description="\n\n".join(
                self.config["commandList"]["moderation"]), inline=True)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Unknown Help Category -", description=f"{args[0]} is not a category.")
            await ctx.send(embed=embed)


    @commands.command()
    async def info(self, ctx):
        prefix = self.config["prefix"]
        botName = self.config["botName"]
        hexInt = int(random.choice(list(self.config["colors"])), 16)

        embed = discord.Embed(title=f"{botName} Bot Info", color=hexInt)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Built by:", value="viargentum#3850", inline=False)
        embed.add_field(name="Issues or suggestions:", value=f"If you have any issues or suggestions, use {prefix}report or"
                                                            f" create an issue on "
                                                            f"https://www.github.com/viargentum/lucid-bot",
                        inline=False)

        await ctx.send(embed=embed)


    @commands.command(aliases=["purchase", "apply"])
    async def buy(self, ctx):
        embed = discord.Embed(title="Lucid Applications -", description="All customers looking to purchase or be granted "
                                                                        "a slot may apply at the following link "
                                                                        "-\n\nhttps://forms.gle/PT4XdKvVA68hv1ao9",
                            color=0xff0000)

        await ctx.send(embed=embed)
