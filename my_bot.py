import os
import sys

import twitchio.ext.commands.errors
from twitchio.ext import commands
import mini_game
import random
from dotenv import dotenv_values
import songrequest
import scoreboard

# accessing sensitive information through .env
config = dotenv_values(".env")
twitch_oauth_token = config["TWITCH_OAUTH_TOKEN"]
channels_to_connect = config["CHANNELS_TO_CONNECT"]
bot_owner = config["BOT_OWNER"]


# a list for a game of rock, scissors and paper
rock_scissors_paper = ["rock", "scissors", "paper"]

class Bot(commands.Bot):
    game_active = False
    game_word = "beep boop"

    def __init__(self):
        # Access token, command prefix, and the channels to be connected.
        super().__init__(token=twitch_oauth_token,
                         prefix="#",
                         initial_channels=[channels_to_connect])

    async def event_ready(self):
        """Bot is logged into these channels' chats."""
        print(f"{self.nick} is connected to the {self.connected_channels}.")
        # Informs the chat.
        await bot.connected_channels[0].send("I have arrived.")

    # shows users who join the chat in the terminal window
    async def event_join(self, channel: channels_to_connect, user):
        print(f"{user.name} has joined the chat.")

    async def event_message(self, message):
        """This function receives messages in Twitch chat"""
        # ignore messages by the bot unless it is part of the mini-game
        if message.echo and message.content != f"{self.game_word}":
            return
        # just to let the user know about a game starting (can be removed)
        elif message.echo and message.content == f"{self.game_word}":
            print("A mini-game has just started")
        # if the game is active, pass the messages sent as an argument to the mini-game.
        if self.game_active:
            await mini_game.mini_game(message)
            # shows the messages in the terminal
        else:
            print(f"{message.author.name} : {message.content}")

            # Returns the greetings of a user
            user_greetings = ("hello", "hi", "hey", "heyguys", "yo")
            if message.content.casefold() in user_greetings:
                await message.channel.send(f"HeyGuys  {message.author.mention}")

            # receives messages and responses to commands.
            await self.handle_commands(message)

    # shutdown the bot from the chat
    async def close(self):
        sys.exit(0)

    """Commands are found here"""
    @commands.command()
    async def hello(self, context: commands.Context):
        # Greet the user
        if context.author.name != f"{bot_owner}".lower():
            await context.send(f"Hello {context.author.name}! Type #rock/#scissors/#paper "
                               f"if you would like to play with me!")
        else:
            await context.send(f"Hello there, boss!")

    @commands.command()
    async def rock(self, context: commands.Context):
        """Plays rock, paper, scissors"""
        bot_choice = random.choice(rock_scissors_paper)
        await context.send(f"I choose...")
        match bot_choice:
            case "rock":
                await context.send(f"{bot_choice.upper()}. Looks like it's a tie.")
            case "scissors":
                await context.send(f"{bot_choice.upper()}. You win this time.")
            case "paper":
                await context.send(f"{bot_choice.upper()}. Imagine losing to a bot. KEKW")

    @commands.command()
    async def scissors(self, context: commands.Context):
        """Plays rock, scissors, paper"""
        bot_choice = random.choice(rock_scissors_paper)
        await context.send(f"I choose...")
        match bot_choice:
            case "rock":
                await context.send(f"{bot_choice.upper()}. Get rekt KEKW")
            case "scissors":
                await context.send(f"{bot_choice.upper()}. No winners.")
            case "paper":
                await context.send(f"{bot_choice.upper()}. You won.")

    @commands.command()
    async def paper(self, context: commands.Context):
        """Plays rock, scissors, paper"""
        bot_choice = random.choice(rock_scissors_paper)
        await context.send(f"I choose...")
        match bot_choice:
            case "rock":
                await context.send(f"{bot_choice.upper()}. You won.")
            case "scissors":
                await context.send(f"{bot_choice.upper()}. EZ win.")
            case "paper":
                await context.send(f"{bot_choice.upper()}. Tie. Go again.")

    @commands.command()
    async def shutdown(self, context: commands.Context):
        """turn the bot off from the chat"""
        if context.author.name != f"{bot_owner}".lower():
            await context.send(f"You have no power here.")
        else:
            await context.send(f"{bot_owner} wants me gone. Goodbye :(")
            await self.close()

    @commands.command()
    async def score(self, context: commands.Context):
        """check the score for the mini-game with #score in the chat"""
        try:
            user = context.author.name
            score = scoreboard.Score(user)
            point = await score.get_score(user)
            await context.send(f"{context.author.mention} has {point} points.")
        # if no local file has been located
        except FileNotFoundError:
            await context.send(f"There was a problem with the scoreboard.")

    @commands.cooldown(rate=1, per=5)
    @commands.command(aliases= ["songrequest"])
    async def sr(self, context: commands.Context):
        try:
            sr_ins = songrequest.Playlist()
            playlist_id = await sr_ins.make_playlist()
            # parse user command to get the youtube link.
            # if they use #sr
            if "#sr" in context.message.content[:3]:
                link = context.message.content[4:]
            #else it must be #songrequest
            else:
                link = context.message.content[13:]
            try:
                await songrequest.song_request(playlist_id, link)
                await context.send(f"{context.author.mention}'s song added to playlist.")
            except Exception as e:
                await context.send("I cannot play that link. Make sure it is a valid YouTube link.")
                print(e)
        except twitchio.ext.commands.errors.CommandOnCooldown as cooldown_error:
            await context.send("Command is on cooldown.")

# instantiate the Bot class
bot = Bot()
