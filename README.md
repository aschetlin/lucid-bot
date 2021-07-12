
# Table of Contents

1.  [Lucid Discord Bot](#orga3f3649)
2.  [Installation](#orga1a76f0)
3.  [Commands](#org6bcfb3d)


<a id="orga3f3649"></a>

# Lucid Discord Bot

Lucid is a fully open-source, general purpose moderation and administration
discord bot build in discord.py.

The bot is built to make self-hosting very easy, including hosting multiple
instances of the bot at once.


<a id="orga1a76f0"></a>

# Installation

****NOTE****:
  If you haven't already, create a Discord application and bot using the
  [Discord Developer Portal](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwig4ciE6vbwAhVtKFkFHSblAl8QjBAwAXoECAYQAQ&url=https%3A%2F%2Fdiscord.com%2Fdevelopers%2Fdocs%2Fgame-sdk%2Fapplications&usg=AOvVaw3b3k10Sxsuc8oMzbYe7LXZ). A guide on how to do so can be found [here](https://discordpy.readthedocs.io/en/latest/discord.html).
  Ensure that your bot application has the **server members intent** enabled,
  like [this](https://i.gyazo.com/2ed5db988dbd486030ae453497cc61ad.png).

To install Lucid, begin by cloning the repository:

    $ git clone https://github.com/viargentum/lucid-bot

Then, copy the config.json file found in the examples directory to your
working directory:

    $ cp examples/config.json .

Fill in all of the empty values, including your bot token.

The suggested way to run Lucid is through **docker** and **docker-compose**.
Ensure you have the latest installations of docker and docker-compose,
and the docker daemon is running. Then run:

    $ docker-compose up --build -d

This will start a new daemonized compose network with the bot and
redis containers. If you've followed these steps correctly, you should
be done. You can check if the containers are running with:

    $ docker ps

It should show that two containers are running.

To stop the bot at any time, make sure you're in the working directory,
and run:

    $ docker-compose stop

This will persist your redis db data. If you would like to completely
reset the bot and its db, run:

    $ docker-compose down


<a id="org6bcfb3d"></a>

# Commands

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Command</th>
<th scope="col" class="org-left">Permission</th>
<th scope="col" class="org-left">Usage</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">announce</td>
<td class="org-left">administrator</td>
<td class="org-left">,announce</td>
</tr>


<tr>
<td class="org-left">ban</td>
<td class="org-left">ban<sub>members</sub></td>
<td class="org-left">,ban @user OR ,ban</td>
</tr>


<tr>
<td class="org-left">editlog</td>
<td class="org-left">administrator</td>
<td class="org-left">,editlog (,help for more)</td>
</tr>


<tr>
<td class="org-left">help</td>
<td class="org-left">N/A</td>
<td class="org-left">,help</td>
</tr>


<tr>
<td class="org-left">info</td>
<td class="org-left">N/A</td>
<td class="org-left">,info</td>
</tr>


<tr>
<td class="org-left">kick</td>
<td class="org-left">kick<sub>members</sub></td>
<td class="org-left">,kick @user OR ,kick</td>
</tr>


<tr>
<td class="org-left">lockdown</td>
<td class="org-left">manage<sub>channels</sub></td>
<td class="org-left">,lockdown OR ,lockdown lift</td>
</tr>


<tr>
<td class="org-left">mute</td>
<td class="org-left">kick<sub>members</sub></td>
<td class="org-left">,mute @user OR ,mute</td>
</tr>


<tr>
<td class="org-left">ping</td>
<td class="org-left">N/A</td>
<td class="org-left">,ping</td>
</tr>


<tr>
<td class="org-left">profile</td>
<td class="org-left">N/A</td>
<td class="org-left">,profile &lt;username&gt;</td>
</tr>


<tr>
<td class="org-left">purge</td>
<td class="org-left">manage<sub>messages</sub></td>
<td class="org-left">,purge &lt;amount&gt;</td>
</tr>


<tr>
<td class="org-left">reload</td>
<td class="org-left">is<sub>bot</sub><sub>owner</sub></td>
<td class="org-left">,reload &lt;cog&gt;</td>
</tr>


<tr>
<td class="org-left">report</td>
<td class="org-left">N/A</td>
<td class="org-left">,report</td>
</tr>


<tr>
<td class="org-left">repost</td>
<td class="org-left">administrator</td>
<td class="org-left">,repost (,help for more)</td>
</tr>


<tr>
<td class="org-left">say</td>
<td class="org-left">manage<sub>messages</sub></td>
<td class="org-left">,say &lt;message&gt;</td>
</tr>


<tr>
<td class="org-left">slowmode</td>
<td class="org-left">manage<sub>channels</sub></td>
<td class="org-left">,slowmode OR ,slowmode lift</td>
</tr>


<tr>
<td class="org-left">unban</td>
<td class="org-left">ban<sub>members</sub></td>
<td class="org-left">,unban &lt;id&gt;</td>
</tr>


<tr>
<td class="org-left">unmute</td>
<td class="org-left">kick<sub>members</sub></td>
<td class="org-left">,unmute @user OR ,unmute</td>
</tr>
</tbody>
</table>

