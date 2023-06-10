## Twitch Bot made using TwitchIO
### by Salim Ege Caliskan

Note: Add your twitch oauth token (a variable named "TWITCH_OAUTH_TOKEN"), as well as the list of channels to be connected (a list named "CHANNELS_TO_CONNECT"), as well as the "BOT_OWNER" into ".env"

This is a hobby project I am currently coding, using TwitchIO, as
I wanted to make a bot for a friend who streams.

At the moment it can be used to play an interactive game of Rock, Paper, and Scissors.
It also reminds the audience to follow the stream and to hydrate, and greets a chatter based on a message they send.
There is also a mini game that occurs randomly between 25 and 55 minutes, where the bot sends "beep boop" into the chat, and the first person to type "beep boop" wins.

And maybe add more words that can be randomly chosen by the bot.

I intend to add Spotify functionality so that moderators can play (and perhaps, skip) songs, turn the volume up/down.

I also want to look into automate modding the chat based on some forbidden words, and detect bots spamming.

Lastly, I might implement some commands that could answer some questions/requests from the viewers about the game the streamer is playing.

### In progress:

Began implementing Youtube song request function. The user needs to 1) get their API key, 2) channel ID key and store them in .env as "YOUTUBE_API_KEY" and "YOUTUBE_CHANNEL_ID" respectively.
Next, the user needs to get their clients secret from Google services (they will most likely need to give access to their channel as test users as well), and download the json file and rename it to ".clients_secret.json".
The credentials will then be saved for any future use.

### Done:
Users can now check their wins in the chat. The scores are kept locally in a json file. (#score command added.)