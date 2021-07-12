from json.decoder import JSONDecodeError
import requests
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed


class Profile(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="profile")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _profile(self, ctx: commands.Context, name: str) -> None:
        with requests.get(
            f"https://api.mojang.com/users/profiles/minecraft/{name}"
        ) as r:
            try:
                uuid: str = r.json().get("id")
                uname: str = r.json().get("name")

            except JSONDecodeError:
                await ctx.message.add_reaction("❌")
                return

        embed = (
            lucid_embed(ctx, success=True, title="Minecraft Profile Query -")
            .add_field(name="Username:", value=uname)
            .add_field(name="UUID:", value=uuid, inline=False)
            .add_field(
                name="Skin URL:",
                value=f"[link](https://crafatar.com/skins/{uuid})",
                inline=False,
            )
            .set_thumbnail(url=f"https://crafatar.com/renders/body/{uuid}?overlay")
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
