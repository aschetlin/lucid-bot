import redis
from discord.ext import commands
from lucid_bot import config
from lucid_bot.lucid_embed import lucid_embed


class EditLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.config
        self.redis = redis.Redis(
            host=self.config["redis"]["hostname"],
            port=self.config["redis"]["port"],
            db=self.config["redis"]["db"],
            decode_responses=True,
        )

    @commands.group(name="editlog", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def _editlog(self):
        raise commands.CommandNotFound

    @_editlog.command(name="status")
    async def _editlog_status(self, ctx):
        embed = (
            lucid_embed(title="Editlog Status -")
            .add_field(
                name="Active:",
                value=self.redis.hget(ctx.guild.id, "editLogActive"),
            )
            .add_field(
                name="Log Channel:",
                value=self.redis.hget(ctx.guild.id, "editLogChannel"),
                inline=False,
            )
        )
        await ctx.send(embed=embed)

    @_editlog.command(name="activate")
    async def _editlog_activate(self, ctx):
        self.redis.hmset(ctx.guild.id, {"editLogActive": "True"})
        await ctx.message.add_reaction("✅")

    @_editlog.command(name="deactivate")
    async def _editlog_deactivate(self, ctx):
        self.redis.hmset(ctx.guild.id, {"editLogActive": "False"})
        await ctx.message.add_reaction("✅")

    @_editlog.command(name="channel")
    async def _editlog_channel(self, ctx, channel_id):
        try:
            channel = self.bot.get_channel(int(channel_id))

        except ValueError:
            await ctx.message.add_reaction("❌")
            return

        if channel is None:
            await ctx.message.add_reaction("❌")

        else:
            self.redis.hmset(ctx.guild.id, {"editLogChannel": channel_id})
            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(EditLog(bot))
