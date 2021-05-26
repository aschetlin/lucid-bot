import discord
import redis
from discord.ext import commands
from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


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

    @commands.group(name="repost", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def _repost(self, ctx):
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
                value=self.redis.hget(ctx.guild.id, "repostTargetChannel"),
                inline=False,
            )
        )
        await ctx.send(embed=embed)

    @_repost.command(name="activate")
    async def _repost_activate(self, ctx):
        self.redis.hmset(ctx.guild.id, {"repostActive": "True"})
        await ctx.message.add_reaction("✅")

    @_repost.command(name="deactivate")
    async def _repost_deactivate(self, ctx):
        self.redis.hmset(ctx.guild.id, {"repostActive": "False"})
        await ctx.message.add_reaction("✅")

    @_repost.command(name="user")
    async def _repost_user(self, ctx, user_id: int):
        try:
            await self.bot.fetch_user(user_id)

        except (discord.NotFound, discord.HTTPException):
            await ctx.send(f"User with ID {user_id} could not be found.")
            return

        self.redis.hmset(ctx.guild.id, {"repostTargetUser": int(user_id)})
        await ctx.message.add_reaction("✅")

    @_repost.command(name="channel")
    async def _repost_channel(self, ctx, channel_id: int):
        try:
            self.bot.get_channel(channel_id)

        except (discord.NotFound, discord.HTTPException):
            await ctx.send(
                f"Channel with ID {channel_id} could not be found."
            )
            return

        self.redis.hmset(
            ctx.guild.id, {"repostTargetChannel": int(channel_id)}
        )
        await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Repost(bot))
