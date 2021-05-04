import asyncio

import discord
from discord.ext import commands
from lucid_bot.lucid_embed import lucid_embed


class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *args):
        if not args:
            embed = lucid_embed(
                ctx,
                title="Unban -",
                description="Which user should be unbanned?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    unbanMsg = await self.bot.wait_for("message", timeout=15)

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if unbanMsg.author.id == ctx.author.id:
                    await unbanMsg.delete()
                    try:
                        unbanUser = await self.bot.fetch_user(
                            int(unbanMsg.content)
                        )
                        await ctx.guild.unban(unbanUser)

                        embed = lucid_embed(ctx, success=True).set_author(
                            name=f"| Successfully unbanned {unbanMsg.mentions[0]}.",
                            icon_url="https://i.imgur.com/4yUeOVj.gif",
                        )
                        await message.edit(embed=embed)

                        return None

                    # except IndexError:
                    #     embed = Embed(
                    #         ctx,
                    #         fail=True,
                    #         title="Unban Failed -",
                    #         description="Did you mention a user?",
                    #     )
                    #     await message.edit(embed=embed)

                    #     return None

                    except discord.errors.Forbidden:
                        embed = lucid_embed(
                            ctx,
                            fail=True,
                            title="Permissions Error -",
                            description="Are you trying to ban another "
                            "moderator/administrator?",
                        )
                        await message.edit(embed=embed)

                        return None
        else:

            try:
                await ctx.message.mentions[0].unban()
                await ctx.message.delete()

                embed = lucid_embed().set_author(
                    ctx,
                    success=True,
                    name=f"| Successfully unbanned {ctx.message.mentions[0]}.",
                    icon_url="https://i.imgur.com/4yUeOVj.gif",
                )
                await ctx.send(embed=embed)

                return None

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Unban Failed -",
                    description="IndexError: Did you mention a valid "
                    "user?",
                )
                await ctx.send(embed=embed)

            # except discord.Forbidden:
            #     embed = Embed(
            #         ctx,
            #         fail=True,
            #         title="Permissions Error -",
            #         description="Are you trying to ban another "
            #         "moderator/administrator?",
            #     )
            #     await ctx.send(embed=embed)
