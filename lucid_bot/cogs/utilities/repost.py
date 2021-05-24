import json
from lucid_bot.lucid_embed import lucid_embed
import discord
import redis
from discord.ext import commands
from lucid_bot import config


class Repost(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.config = config.config
        self.redis = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
            decode_responses=True,
        )

    @commands.command(name="repost")
    @commands.is_owner()
    async def _repost(self, ctx, *args):
        if args[0] == "status":

            embed = (
                lucid_embed(ctx, title="Chat Reposter Status: ")
                .add_field(
                    name="Active:",
                    value=self.redis.hget(ctx.guild.id, "repostActive"),
                )
                .add_field(
                    name="Target User:",
                    value=self.redis.hget(ctx.guild.id, "repostTargetUser"),
                    inline=False,
                )
                .add_field(
                    name="Target Channel:",
                    value=self.redis.hget(
                        ctx.guild.id, "repostTargetChannel"
                    ),
                    inline=False,
                )
            )
            await ctx.send(embed=embed)

        elif args[0] == "activate":
            self.redis.hmset(ctx.guild.id, {"repostActive": "True"})
            await ctx.message.add_reaction("✅")

        elif args[0] == "deactivate":
            self.redis.hmset(ctx.guild.id, {"repostActive": "False"})
            await ctx.message.add_reaction("✅")

        elif args[0] == "user":
            try:
                await self.bot.fetch_user(args[1])

            except (discord.NotFound, discord.HTTPException):
                await ctx.send(
                    f"User with ID {args[1]} could not be found."
                )
                return

            self.redis.hmset(
                ctx.guild.id, {"repostTargetUser": str(args[1])}
            )
            await ctx.message.add_reaction("✅")

        elif args[0] == "channel":
            try:
                self.bot.get_channel(int(args[1]))

            except (discord.NotFound, discord.HTTPException):
                await ctx.send(
                    f"Channel with ID {args[1]} could not be found."
                )
                return

            self.redis.hmset(
                ctx.guild.id, {"repostTargetChannel": str(args[1])}
            )
            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Repost(bot))
