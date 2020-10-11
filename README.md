# Lucid Discord Bot

This is a fully open-source, general purpose moderation and administration discord bot built in discord.py.

The bot is built to make self-hosting very easy, but also allow hosting multiple instances of the bot at once with minimal effort.

# Installation/Setup
**If you haven't already, create a discord application and bot using the Discord Developer Portal. A guide on how to do so can be found [here](https://discordpy.readthedocs.io/en/latest/discord.html).**

Ensure that your bot application has the **server members intent** enabled:![enter image description here](https://watch.femboi.porn/the_goods/7aba50b8.png)

To setup Lucid, begin by cloning the directory:

    $ git clone https://github.com/Viargentum/lucid-bot
   Copy the config.json file found in the examples directory to the lucid-bot directory, and replace any empty keys with the corresponding value. **(if you dont plan on running multiple instances of the bot at once, you can ignore the "redis" key).**

To start a single instance of the bot, run the *main.py*:

**Windows:**

    $ .\main.py
   
**Linux**:
   Making main.py executable (only on first run):
	
    $ chmod 777 ./main.py
   Running main.py:
   
    $ ./main.py

## Running multiple instances in parallel

To run multiple instances of the bot in parallel, you can begin by running a default instance, as seen above.
Then, in a new environment or screen, you will need to edit the environment variables:

**Windows:**

    $ $env:LUCID_BOT__NAME = 'yourName'
    
    $ $env:LUCID_BOT__PREFIX = 'yourPrefix'
    
    $ $env:LUCID_BOT__TOKEN = 'yourToken'
    
    $ $env:LUCID_BOT__REDIS__DB = '1'
    
    $ .\main.py
    
(for each new instance, you will need to re-define these keys, and add one to the REDIS__DB number)

# Commands

|Permission      |Command                        |Usage                       |
|----------------|-------------------------------|-----------------------------|
|n/a			 |`ping`            			 | ping            |
|n/a             |`help`           				 | help **or** help *category*           |
|n/a	         |`info`						 | info|
|kick_members    |`kick` 						 | kick @user **or** kick
|mute_members	 |`mute`              			 | mute@user **or** mute
|ban_members     |`ban`                          | ban @user **or** ban
|administrator   |`announce`					 | announce
|manage_channels |`lockdown`					 | lockdown **or** lockdown lift
|n/a             |`report`                       | report
