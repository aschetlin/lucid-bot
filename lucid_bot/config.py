import os
import json


configkeys = [k for k in os.environ.keys() if k.lower().startswith("lucid_bot")]
config = json.loads(open("config.json", "r", encoding="utf8").read())

