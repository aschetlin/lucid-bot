import discord
import random
from lucid_bot.config import config
from lucid_bot.bot import bot

bot.remove_command("help")


@bot.command(aliases=["ms", "delay"])
async def ping(ctx):
    pingMsg = await ctx.send("*pinging...*")
    msgPing = round((pingMsg.created_at - ctx.message.created_at).total_seconds() * 1000)

    await pingMsg.delete()
    botPing = round(bot.latency * 1000)
    hexInt = int(random.choice(list(config["colors"])), 16)

    embed = discord.Embed(title="Ping -", color=hexInt)
    embed.add_field(name=f"API Latency:", value=f"~{botPing}ms")
    embed.add_field(name=f"Message Latency:", value=f"~{msgPing}ms")

    await ctx.send(embed=embed)


@bot.command()
async def help(ctx, *args):
    hexInt = int(random.choice(list(config["colors"])), 16)
    botName = config["botName"]

    if not args:
        embed = discord.Embed(title=f"{botName} Bot Help -", color=hexInt, description="use help <category> to get "
                                                                                       "more info")
        embed.add_field(name="Utility -", value="`ping`, `help`, `info`", inline=False)
        embed.add_field(name="General -", value="`report`, `announce`", inline=False)
        embed.add_field(name="Moderation -", value="`kick`, `mute`, `ban`, `slowmode`, `lockdown`", inline=False)

        await ctx.send(embed=embed)

    elif args[0].lower() == "utility":
        embed = discord.Embed(title="Utility Commands Help -", color=hexInt, description="\n\n".join(
            config["commandList"]["utilities"]), inline=True)

        await ctx.send(embed=embed)

    elif args[0].lower() == "general":
        embed = discord.Embed(title="General Commands Help -", color=hexInt, description="\n\n".join(
            config["commandList"]["general"]), inline=True)

        await ctx.send(embed=embed)

    elif args[0].lower() == "moderation":
        embed = discord.Embed(title="Moderation Commands Help -", color=hexInt, description="\n\n".join(
            config["commandList"]["moderation"]), inline=True)

        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Unknown Help Category -", description=f"{args[0]} is not a category.")
        await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    botName = config["botName"]
    hexInt = int(random.choice(list(config["colors"])), 16)

    embed = discord.Embed(title=f"{botName} Bot Info", color=hexInt)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Built by:", value="viargentum#3850", inline=False)
    embed.add_field(name="Issues or suggestions:", value="If you have any issues or suggestions, use the report "
                                                         "command, or create an issue on "
                                                         "https://www.github.com/viargentum/lucid-bot", inline=False)
    await ctx.send(embed=embed)
