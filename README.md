# Lucid Discord Bot

This is a fully open-source, general purpose moderation and administration discord bot built in discord.py.

The bot is built to make self-hosting very easy, but also allow hosting multiple instances of the bot at once with minimal effort.
    
# Commands

|Permission      |Command                        |Usage                       
|----------------|-------------------------------|-----------------------------
|n/a			 |`ping`            			 | ping            
|n/a             |`help`           				 | help **or** help *category*           
|n/a	         |`info`						 | info|
|kick_members    |`kick` 						 | kick @user **or** kick
|mute_members	 |`mute`              			 | mute@user **or** mute
|ban_members     |`ban`                          | ban @user **or** ban
|administrator   |`announce`					 | announce
|manage_channels |`lockdown`					 | lockdown **or** lockdown lift
|manage_channels |`slowmode`                     | slowmode *time(seconds)* **or** slowmode
|n/a             |`report`                       | report

# Installation
**NOTE:** If you haven't already, create a Discord application and bot using the Discord Developer Portal. A guide on how to do so can be found [here](https://discordpy.readthedocs.io/en/latest/discord.html). Ensure that your bot application has the **server members intent** enabled (like [this](https://i.gyazo.com/2ed5db988dbd486030ae453497cc61ad.png)). If you are hosting multiple instances, you will need to clone the repository again into a different location for each instance.

To install Lucid, begin by cloning the repository:

    $ git clone https://github.com/Viargentum/lucid-bot

Then, copy the config.json file found in the examples directory your working directory.

To install the packages required for Lucid Bot to function, you can use pip:

    $ pip install -r requirements.txt
    
If you're using Linux or MacOS, you should also make *main.py* execulable:
	
    $ chmod 777 ./main.py

# Database Setup
#### Windows:
First, download the latest release of Redis [here](https://github.com/microsoftarchive/redis/releases) (make sure you download the *.msi* file). Run and install.
Then, run *redis-cli*:

    $ redis-cli
Disable protected mode:

    > CONFIG SET protected-mode no
Finally, exit from *redis-cli*:

    > exit

#### Linux (Ubuntu/Debian):
First, install *redis-server*:

    $ apt install redis-server
Start Redis:

    $ redis-server
Then, run *redis-cli*:

    $ redis-cli
Disable protected mode:

    > CONFIG SET protected-mode no
Finally, exit from *redis-cli*:

    > exit

# Hosting a single instance
### Using config.json:
First, replace any empty fields in *config.json* with their respective values (this is also the time to change the prefix!)
Then, run the *main.py*:
#### Windows:

    $ .\main.py
#### Linux:
    
    $ ./main.py

### Using environment variables:
#### Windows:
First, edit your environment variables:

    $ $env:LUCID_BOT__NAME = 'yourName'
    $ $env:LUCID_BOT__PREFIX = 'yourPrefix'
    $ $env:LUCID_BOT__TOKEN = 'yourToken'
    $ $env:LUCID_BOT__REDIS__DB = '1'
Then, run the *main.py*:
    
    $ .\main.py
   
#### Linux:
To set the environment variables for the current user, first open your *.bashrc* file:

    $ nano ~/.bashrc
    
Then, append the following lines:
    
    export LUCID_BOT__NAME='yourName'
    export LUCID_BOT__PREFIX='yourPrefix'
    export LUCID_BOT__TOKEN='yourToken'
    export LUCID_BOT__REDIS__DB='1'
    
Now you can save and exit. Lastly, run the *main.py*:

    $ ./main.py
    
# Hosting multiple instances
### Using config.json:
First, make sure you have created multiple separate bot applications on the Discord Developer Portal. Then, replace any empty fields in each *config.json* with their respective values (this is also the time to change the prefixes!)
Then, run the *main.py*:
#### Windows:
    
    $ .\main.py
#### Linux:
    
    $ ./main.py

### Using environment variables:
**NOTE:** You cannot host multiple instances of Lucid on Windows using environment variables as you can't have duplicate keys.
#### Linux:
First, set the environment variables:
    
    $ export LUCID_BOT__NAME='yourName'
    $ export LUCID_BOT__PREFIX='yourPrefix'
    $ export LUCID_BOT__TOKEN='yourToken'
    $ export LUCID_BOT__REDIS__DB='1'
    
Now you can run the *main.py*:

    $ ./main.py

**This is not persistant!** Once you terminate the terminal session the environment variables will be gone.
