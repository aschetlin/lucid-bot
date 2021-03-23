import discord
import random
from lucid_bot.config import config
from lucid_bot.bot import bot, slash, guild_ids
from discord_slash.utils.manage_commands import create_option

bot.remove_command("help")


@slash.slash(name="ping", description="Returns the current API and Message latencies in milliseconds.", guild_ids=guild_ids)
async def ping(ctx):
    await ctx.respond()
    
    pingMsg = await ctx.send(content="*pinging...*")
    msgPing = round((pingMsg.created_at - ctx.message.created_at).total_seconds() * 1000)

    await pingMsg.delete()
    botPing = round(bot.latency * 1000)
    hexInt = int(random.choice(list(config["colors"])), 16)

    embed = discord.Embed(title="Ping -", color=hexInt)
    embed.add_field(name=f"API Latency:", value=f"~{botPing}ms")
    embed.add_field(name=f"Message Latency:", value=f"~{msgPing}ms")

    await ctx.send(embed=embed)


@slash.slash(name="help", description="Returns the help menu for Lucid Bot.", options=[create_option(name="category", description="Select which category to get more info on.", 
                                                                                                                        option_type=3, required=False)], guild_ids=guild_ids)
async def help(ctx, *category: str):
    await ctx.respond()

    if not category:
        pass
    else:
        selectedCategory = category[0]

    prefix = config["prefix"]
    hexInt = int(random.choice(list(config["colors"])), 16)
    botName = config["botName"]

    if not category:
        embed = discord.Embed(title=f"{botName} Bot Help -", color=hexInt, description=f"use {prefix}help <category> "
                                                                                       f"to get more info")
        embed.add_field(name="Utility -", value="`ping`, `help`, `info`, `purchase`", inline=False)
        embed.add_field(name="General -", value="`report`, `announce`, `say`", inline=False)
        embed.add_field(name="Moderation -", value="`kick`, `mute`, `ban`, `slowmode`, `lockdown`", inline=False)

        await ctx.send(embed=embed)

    elif selectedCategory == "utility":
        embed = discord.Embed(title="Utility Commands Help -", color=hexInt, description="\n\n".join(
            config["utilities"]), inline=True)

        await ctx.send(embed=embed)

    elif selectedCategory == "general":
        embed = discord.Embed(title="General Commands Help -", color=hexInt, description="\n\n".join(
            config["general"]), inline=True)

        await ctx.send(embed=embed)

    elif selectedCategory == "moderation":
        embed = discord.Embed(title="Moderation Commands Help -", color=hexInt, description="\n\n".join(
            config["utilities"]), inline=True)

        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Unknown Help Category -", description=f"{selectedCategory} is not a category.")
        await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    prefix = config["prefix"]
    botName = config["botName"]
    hexInt = int(random.choice(list(config["colors"])), 16)

    embed = discord.Embed(title=f"{botName} Bot Info", color=hexInt)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Built by:", value="viargentum#3850", inline=False)
    embed.add_field(name="Issues or suggestions:", value=f"If you have any issues or suggestions, use {prefix}report or"
                                                         f" create an issue on "
                                                         f"https://www.github.com/viargentum/lucid-bot",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=["purchase", "apply"])
async def buy(ctx):
    embed = discord.Embed(title="Lucid Applications -", description="All customers looking to purchase or be granted "
                                                                    "a slot may apply at the following link "
                                                                    "-\n\nhttps://forms.gle/PT4XdKvVA68hv1ao9",
                          color=0xff0000)

    await ctx.send(embed=embed)
