import discord
import asyncio
from lucid_bot.bot import bot
from lucid_bot.config import config
from lucid_bot.non_bot_funcs import yes_no_dialogue


@bot.command(aliases=["raid", "panic"])
async def lockdown(ctx, *args):
    if ctx.author.guild_permissions.manage_channels or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Channel Lockdown -", description="Should all channels or only this channel be "
                                                                          "locked down?\n\n (Yes for all channels, "
                                                                          "no for this channel only.)")
            message = await ctx.send(embed=embed)

            allChannels = await yes_no_dialogue(message, 20, False, ctx)

            if allChannels:
                text_channel_list = []
                guild = ctx.guild

                for channel in guild.text_channels:
                    text_channel_list.append(channel)

                for channel in text_channel_list:
                    await channel.set_permissions(ctx.guild.default_role, send_messages=False)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel lockdown successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

            else:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel lockdown successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

        elif args[0] == "lift".lower():

            embed = discord.Embed(title="Channel Lockdown -", description="Should all channels or only this channel "
                                                                          "be unlocked? \n\n (Yes for all channels, "
                                                                          "no for this channel only.)")
            message = await ctx.send(embed=embed)

            allChannels = await yes_no_dialogue(message, 20, False, ctx)

            if allChannels:
                text_channel_list = []
                guild = ctx.guild

                for channel in guild.text_channels:
                    text_channel_list.append(channel)

                for channel in text_channel_list:
                    await channel.set_permissions(ctx.guild.default_role, send_messages=True)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel unlock successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

            else:
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

                embed = discord.Embed(title="Channel Lockdown -", description="Channel unlock successful.")
                await message.clear_reactions()
                await message.edit(embed=embed)

                return None

        else:
            embed = discord.Embed(title="Command Failed", description="Unknown argument, \"" + args[0] + "\"")
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None


@bot.command()
async def kick(ctx, *args):
    if ctx.author.guild_permissions.kick_members or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Punishment -", description="Which user should be kicked?")
            message = await ctx.send(embed=embed)

            while True:

                try:
                    kickUser = await bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
                    await message.edit(embed=embed)

                    return None

                if kickUser.author.id == ctx.author.id:
                    await kickUser.delete()
                    try:
                        await kickUser.mentions[0].ban()

                        embed = discord.Embed(
                            title="Successfully banned user -", description=kickUser.mentions[0].mention
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = discord.Embed(title="Punishment Failed -", description="Did you mention a user?")
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = discord.Embed(title="Permissions Error -", description="Are you trying to kick another "
                                                                                       "moderator/administrator?")
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                targetUser = ctx.message.mentions[0]
                await targetUser.kick()

            except IndexError:
                embed = discord.Embed(title="Punishment Failed -", description="IndexError: Did you mention a valid "
                                                                               "user?")
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = discord.Embed(title="Permissions Error -", description="Are you trying to kick another "
                                                                               "moderator/administrator?")
                await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None


@bot.command()
async def ban(ctx, *args):
    if ctx.author.guild_permissions.ban_members or ctx.author.id in config["adminIDS"]:

        if not args:
            embed = discord.Embed(title="Punishment -", description="Which user should be banned?")
            message = await ctx.send(embed=embed)

            while True:

                try:
                    banUser = await bot.wait_for("message", timeout=20)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title="Timeout", description="Sorry, you took too long to respond.")
                    await message.edit(embed=embed)

                    return None

                if banUser.author.id == ctx.author.id:
                    await banUser.delete()
                    try:
                        await banUser.mentions[0].ban()

                        embed = discord.Embed(
                            title="Successfully banned user -", description=banUser.mentions[0].mention
                        )
                        await message.edit(embed=embed)

                        return None

                    except IndexError:
                        embed = discord.Embed(title="Punishment Failed -", description="Did you mention a user?")
                        await message.edit(embed=embed)

                        return None

                    except discord.errors.Forbidden:
                        embed = discord.Embed(title="Permissions Error -", description="Are you trying to ban another "
                                                                                       "moderator/administrator?")
                        await message.edit(embed=embed)

                        return None

        else:

            try:
                targetUser = ctx.message.mentions[0]
                await targetUser.ban()

            except IndexError:
                embed = discord.Embed(title="Punishment Failed -", description="IndexError: Did you mention a valid "
                                                                               "user?")
                await ctx.send(embed=embed)

            except discord.Forbidden:
                embed = discord.Embed(title="Permissions Error -", description="Are you trying to ban another "
                                                                               "moderator/administrator?")
                await ctx.send(embed=embed)

    else:
        embed = discord.Embed(title="Permissions Error -", description="You do not have the required " +
                                                                       "permissions to execute this command.")
        await ctx.send(embed=embed)

        return None
