import requests
from discord.ext import commands

from lucid_bot.lucid_embed import lucid_embed


class Profile(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="profile")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def _profile(self, ctx, name):
        with requests.get(f"https://api.minetools.eu/uuid/{name}") as r:
            uuid = r.json().get("id")

        with requests.get(f"https://api.minetools.eu/profile/{uuid}") as r:
            uname = r.json().get("decoded").get("profileName")
            skin_url = (
                r.json()
                .get("decoded")
                .get("textures")
                .get("SKIN")
                .get("url")
            )

        embed = (
            lucid_embed(
                ctx, success=True, title="Minecraft Profile Query -"
            )
            .add_field(name="Username:", value=uname)
            .add_field(name="UUID:", value=uuid, inline=False)
            .add_field(
                name="Skin URL:", value=f"[link]({skin_url})", inline=False
            )
            .set_thumbnail(
                url=f"https://crafatar.com/renders/body/{uuid}?overlay"
            )
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
