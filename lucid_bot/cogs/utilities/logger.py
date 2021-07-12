import redis

from discord.ext import commands
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument

from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
        self.redis = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
            decode_responses=True,
        )

    @commands.group(name="logger", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def _logger(self, ctx):
        try:
            log_channel = int(self.redis.hget(ctx.guild.id, "logChannel"))

        except:
            log_channel = self.redis.hget(ctx.guild.id, "logChannel")

        embed = (
            lucid_embed(title="Logging Status -")
            .add_field(
                name="Edit Log Active:",
                value=self.redis.hget(ctx.guild.id, "editLogActive"),
                inline=False,
            )
            .add_field(
                name="Delete Log Active:",
                value=self.redis.hget(ctx.guild.id, "deleteLogActive"),
                inline=False,
            )
            .add_field(
                name="Join/Leave Log Active:",
                value=self.redis.hget(ctx.guild.id, "joinLeaveLogActive"),
                inline=False,
            )
            .add_field(
                name="Log Channel:",
                value=self.bot.get_channel(log_channel).mention
                if log_channel
                else log_channel,
                inline=False,
            )
        )
        await ctx.send(embed=embed)

    @_logger.command(name="activate")
    async def _logger_activate(self, ctx, log_type: str) -> None:

        if not log_type:
            raise MissingRequiredArgument(log_type)

        log_type = log_type.lower()

        if log_type == "all":
            self.redis.hmset(ctx.guild.id, {"editLogActive": "True"})
            self.redis.hmset(ctx.guild.id, {"deleteLogActive": "True"})
            self.redis.hmset(ctx.guild.id, {"joinLeaveLogActive": "True"})

        elif log_type == "edit":
            self.redis.hmset(ctx.guild.id, {"editLogActive": "True"})

        elif log_type == "delete":
            self.redis.hmset(ctx.guild.id, {"deleteLogActive": "True"})

        elif log_type == "join" or log_type == "leave" or log_type == "joinleave":
            self.redis.hmset(ctx.guild.id, {"joinLeaveLogActive": "True"})

        else:
            raise BadArgument

        await ctx.message.add_reaction("✅")

    @_logger.command(name="deactivate")
    async def _logger_deactivate(self, ctx, log_type: str) -> None:

        if not log_type:
            raise MissingRequiredArgument(log_type)

        log_type = log_type.lower()

        if log_type == "all":
            self.redis.hmset(ctx.guild.id, {"editLogActive": "False"})
            self.redis.hmset(ctx.guild.id, {"deleteLogActive": "False"})
            self.redis.hmset(ctx.guild.id, {"joinLeaveLogActive": "False"})

        elif log_type == "editlog" or log_type == "edit":
            self.redis.hmset(ctx.guild.id, {"editLogActive": "False"})

        elif log_type == "deletelog" or log_type == "delete":
            self.redis.hmset(ctx.guild.id, {"deleteLogActive": "False"})

        elif log_type == "join" or log_type == "leave" or log_type == "joinleave":
            self.redis.hmset(ctx.guild.id, {"joinLeaveLogActive": "False"})

        else:
            raise BadArgument

        await ctx.message.add_reaction("✅")

    @_logger.command(name="channel")
    async def _logger_channel(self, ctx, channel_id):
        try:
            channel = self.bot.get_channel(int(channel_id))

        except ValueError:
            await ctx.message.add_reaction("❌")
            return

        if channel is None:
            await ctx.message.add_reaction("❌")

        else:
            self.redis.hmset(ctx.guild.id, {"logChannel": channel_id})
            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Logger(bot))
