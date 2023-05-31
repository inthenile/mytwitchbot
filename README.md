## Twitch Bot made using TwitchIO
### by Salim Ege Caliskan

Note: Add your twitch oauth token (a variable named "TWITCH_OAUTH_TOKEN"), as well as the list of channels to be connected (a list named "CHANNELS_TO_CONNECT"), as well as the "BOT_OWNER" into ".env"
If you want to use "spotify.py", you need to retrieve your client_id and client_secret from "https://developer.spotify.com/" and store them within the ".env" folder accordingly.

This is a hobby project I am currently coding, using TwitchIO, as
I wanted to make a bot for a friend who streams.

At the moment it can be used to play an interactive game of Rock, Paper, and Scissors.
It also reminds the audience to follow the stream and to hydrate.

I intend to add Spotify functionality so that moderators can play (and perhaps, skip) songs, turn the volume up/down.
The current "spotify.py" is incomplete; I am working on it. It requires a premium Spotify account to be used.

I also want to look into automate modding the chat based on some forbidden words, and detect bots spamming.

Lastly, I might implement some commands that could answer some questions/requests from the viewers about the game the streamer is playing.

