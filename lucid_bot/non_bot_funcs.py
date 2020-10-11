import asyncio
import discord
from lucid_bot.bot import bot


async def yes_no_dialogue(message_name: discord.Message, timeout: int, dm: bool, ctx) -> object:
    await message_name.add_reaction("✅")
    await message_name.add_reaction("❌")

    while True:

        try:
            reaction = await bot.wait_for("reaction_add", timeout=timeout)

        except asyncio.TimeoutError:
            embed = discord.Embed(title="Timeout -", description="Sorry, you took too long to react.")

            if dm:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send(embed=embed)

            return None

        if reaction[1].id == ctx.author.id:
            reaction = reaction[0].emoji

            if reaction == "✅" or "❌":
                break

            else:
                return None

    if reaction == "✅":
        return True
    else:
        return False
