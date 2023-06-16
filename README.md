## Twitch Bot made using TwitchIO

### by Salim Ege Caliskan


Note: Add your twitch oauth token (a variable named "TWITCH_OAUTH_TOKEN"), as well as the list of channels to be connected (a list named "CHANNELS_TO_CONNECT"), as well as the "BOT_OWNER" into ".env"

This is a hobby project I am currently coding, using TwitchIO, as
I wanted to make a bot for a friend who streams (which makes the bot rather optimised for Guild Wars 2 streams).

    Current commands:
    #build / #builds / #addbuild / #updatebuild / #removebuild (built for Guild Wars 2)
    #rock / #paper / #scissors
    #shutdown
    #score (for the chat minigame)
    #currentsong (outputs the currently playing Spotify song) / #refreshtoken

<strong>Possible to do:</strong>

And maybe add more words that can be randomly chosen by the bot.

*I intend to add Spotify functionality so that moderators can play (and perhaps, skip) songs, turn the volume up/down.* <strong>(in progress)</strong>

I also want to look into automate modding the chat based on some forbidden words, and detect bots spamming.

Lastly, I might implement some commands that could answer some questions/requests from the viewers about the game the streamer is playing.

### Done:
<ul>
    <li>Users can now check their wins in the chat. The scores are kept locally in a json file. (#score command added.)</li>
    <li> Added a Build class, which helps the user save Guild Wars 2 builds. It is fairly simple: it merely writes onto a json file, which consists of key-value pairs.
    Keys are the class/build names which are then used as a twitch chat command to bring up the build (which is a URL). For functions check builds.py</li>
    <li>Started reimplementing Spotify API. It has better functionality than what YouTube offers. Also I have implemented this feature completely on my own,
    whereas for the YouTube connection I copy-pasted a bunch of code, and that did not feel like an accomplishment at all. Right now, I only implemented a command to get the current song. Other features will follow. </li>
</ul>
    
    