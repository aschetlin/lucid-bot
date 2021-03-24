import os
import json


configkeys = [k for k in os.environ.keys() if k.startswith("LUCID_BOT")]
config = json.loads(open("./config.json", "r", encoding="utf8").read())

if "LUCID_BOT__TOKEN" in configkeys:
    config["token"] = os.environ["LUCID_BOT__TOKEN"]

if "LUCID_BOT__PREFIX" in configkeys:
    config["prefix"] = os.environ["LUCID_BOT__PREFIX"]

if "LUCID_BOT__REDIS__DB" in configkeys:
    config["redis"]["db"] = os.environ["LUCID_BOT__REDIS__DB"]

if "LUCID_BOT__NAME" in configkeys:
    config["botName"] = os.environ["LUCID_BOT__NAME"]
