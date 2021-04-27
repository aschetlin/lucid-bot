from lucid_bot.cogs import events
from lucid_bot.cogs.general import announce, report, say
from lucid_bot.cogs.moderation import ban, kick, mute, purge, slowmode, unban, unmute
from lucid_bot.cogs.utilities import help, info, ping

cogs = [
    {"class": events.Events, "config": True},
    {"class": announce.Announce, "nbf": True, "config": True} ,
    {"class": report.Report, "nbf": True, "config": True},
    {"class": say.Say},
    {"class": ban.Ban},
    {"class": kick.Kick},
    {"class": mute.Mute},
    {"class": purge.Purge},
    {"class": slowmode.Slowmode},
    {"class": unban.Unban},
    {"class": unmute.Unmute},
    {"class": help.Help, "config": True},
    {"class": info.Info, "config": True},
    {"class": ping.Ping, "config": True},
]
