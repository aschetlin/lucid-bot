import asyncio

from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed


class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, ctx, *args):
        if not args:
            embed = lucid_embed(
                ctx,
                title="Channel Slowmode -",
                description="How long should the message cool-down be?",
            )
            message = await ctx.send(embed=embed)

            while True:

                try:
                    slowmodeTime = await self.bot.wait_for(
                        "message", timeout=20
                    )

                except asyncio.TimeoutError:
                    embed = lucid_embed(
                        ctx,
                        fail=True,
                        title="Timeout Error -",
                        description="Sorry, you took too long to respond.",
                    )
                    await message.edit(embed=embed)

                    return None

                if slowmodeTime.author.id == ctx.author.id:
                    await slowmodeTime.delete()
                    await ctx.channel.edit(
                        slowmode_delay=slowmodeTime.content
                    )

                    embed = lucid_embed(
                        ctx,
                        success=True,
                        title="Channel Slowmode -",
                        description=f"{slowmodeTime.content}s slowmode activated!",
                    )

                    await message.edit(embed=embed)

                    return None

        if str(args[0]) == "lift":
            await ctx.channel.edit(slowmode_delay=0)

            embed = lucid_embed(
                ctx,
                success=True,
                title="Channel Slowmode -",
                description="Slowmode lifted!",
            )
            await ctx.send(embed=embed)

        else:

            try:
                slowmodeTime = args[0]

                await ctx.channel.edit(slowmode_delay=slowmodeTime)

                embed = lucid_embed(
                    ctx,
                    success=True,
                    title="Channel Slowmode -",
                    description=f"{slowmodeTime}s slowmode activated!",
                )
                await ctx.send(embed=embed)

            except IndexError:
                embed = lucid_embed(
                    ctx,
                    fail=True,
                    title="Channel Slowmode -",
                    description="Invalid slowmode time.",
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Slowmode(bot))
