import json
import sys
import twitchio.ext.commands.errors
from twitchio.ext import commands
import random
from dotenv import dotenv_values
from utility import songrequest
from game import scoreboard, mini_game
from gw2builds import builds

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
                               f"if you would like to play!")
        else:
            await context.send(f"Hello there, boss!")

# CHAT GAME RELATED COMMANDS ###
    @commands.cooldown(rate=1, per=10)
    @commands.command()
    async def rock(self, context: commands.Context):
        """Plays rock, paper, scissors"""
        try:
            bot_choice = random.choice(rock_scissors_paper)
            await context.send(f"I choose...")
            match bot_choice:
                case "rock":
                    await context.send(f"{bot_choice.upper()}. Looks like it's a tie.")
                case "scissors":
                    await context.send(f"{bot_choice.upper()}. You win this time.")
                case "paper":
                    await context.send(f"{bot_choice.upper()}. Imagine losing to a bot. KEKW")
        except twitchio.ext.commands.errors.CommandOnCooldown:
            pass
    @commands.cooldown(rate=1, per=10)
    @commands.command()
    async def scissors(self, context: commands.Context):
        """Plays rock, scissors, paper"""
        try:
            bot_choice = random.choice(rock_scissors_paper)
            await context.send(f"I choose...")
            match bot_choice:
                case "rock":
                    await context.send(f"{bot_choice.upper()}. Get rekt KEKW")
                case "scissors":
                    await context.send(f"{bot_choice.upper()}. No winners.")
                case "paper":
                    await context.send(f"{bot_choice.upper()}. You won.")
        except twitchio.ext.commands.errors.CommandOnCooldown:
            pass
    @commands.cooldown(rate=1, per=10)
    @commands.command()
    async def paper(self, context: commands.Context):
        """Plays rock, scissors, paper"""
        try:
            bot_choice = random.choice(rock_scissors_paper)
            await context.send(f"I choose...")
            match bot_choice:
                case "rock":
                    await context.send(f"{bot_choice.upper()}. You won.")
                case "scissors":
                    await context.send(f"{bot_choice.upper()}. EZ win.")
                case "paper":
                    await context.send(f"{bot_choice.upper()}. Tie. Go again.")
        except twitchio.ext.commands.errors.CommandOnCooldown:
            pass

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

# HERE ARE BUILD SPECIFIC COMMANDS - some commands can only be used by the bot and the channel owner(s)###
    @commands.command()
    async def build(self,context: commands.Context):
        """ displays currently saved builds"""
        try:
            await context.send(await builds.build.currently_available_builds())
        except json.decoder.JSONDecodeError or AttributeError:
            await context.send("There was an error with the build file in the system."
                               " Delete the file and run the command again.")

    @commands.command(aliases=["addbuild"])
    async def newbuild(self, context: commands.Context):
        """saves a new build"""
        if context.author.name.lower() == f"{bot.connected_channels[0].name}".lower()\
                or context.author.name.lower() == f"{bot_owner}".lower():
            # message[0] is #newbuild, and since new_build(name, url) requires three parameters
            # we get them by splitting the chat command
            try:
                message = context.message.content.split(" ")
                class_name = message[1]
                build_name = message[2]
                url = message[3]
                response = await builds.build.new_build(class_name, build_name, url)
                await context.send(response)
            except IndexError or TypeError:
                await context.send("There was an error. Please try again. Double check your parameters."
                                   " #updatebuild class_name  build_name  new_link")
            except json.decoder.JSONDecodeError:
                await context.send("There was an error with the build file in the system."
                                   " Delete the file and run the command again.")
        else:
            await context.send("You cannot use this command.")

    @commands.command(aliases=["deletebuild"])
    async def removebuild(self, context: commands.Context):
        """ deletes an existing build"""
        if context.author.name.lower() == f"{bot.connected_channels[0].name}".lower()\
                or context.author.name.lower() == f"{bot_owner}".lower():
            message = context.message.content.split(" ")
            # message[0] is #newbuild, and since new_build(name, url)
            # requires two parameters, we get the other two by splitting)
            try:
                class_name = message[1]
                build_name = message[2]
                response = await builds.build.delete_build(class_name, build_name)
                await context.send(response)
            except IndexError or TypeError:
                await context.send("There was an error with the command. Type each parameter as a single word,"
                                   "without spaces. E.g. #deletebuild  elementalist  staff-backline")
            except json.decoder.JSONDecodeError:
                await context.send("There was an error with the build file in the system."
                                   " Delete the file and run the command again.")
        else:
            await context.send("You cannot use this command.")
    @commands.command()
    async def updatebuild(self, context: commands.Context):
        if context.author.name.lower() == f"{bot.connected_channels[0].name}".lower()\
                or context.author.name.lower() == f"{bot_owner}".lower():
            # message[0] is updated build, and since update_build(class_name, build_name, url)
            # requires three parameters, we get them by splitting the user command)
            try:
                message = context.message.content.split(" ")
                class_name = message[1]
                build_name = message[2]
                url = message[3]
                response = await builds.build.update_build(class_name, build_name, url)
                await context.send(response)
            except IndexError or TypeError:
                await context.send("There was an error. Please try again. Double check your parameters."
                                   " #updatebuild  class_name  build_name  new_link")
            except json.decoder.JSONDecodeError:
                await context.send("There was an error with the build file in the system."
                                   " Delete the file and run the command again.")
        else:
            await context.send("You cannot use this command.")
    @commands.command(aliases=["showbuilds"])
    async def builds(self, context:commands.Context):
        # message[0] is #newbuild, and since new_build(name, url)
        # requires two parameters, we get the other two by splitting)
        try:
            message = context.message.content.split(" ")
            build_name = message[1]
            response = await builds.build.show_build(build_name)
            await context.send(response)
        except IndexError as error:
            print(error)
            await context.send("Don't forget to add the class name after the command =>"
                               " '#builds necromancer' Check #build to see all available builds.")
        except json.decoder.JSONDecodeError:
            await context.send("There was an error with the build file in the system."
                               " Delete the file and run the command again.")

# MISCELLANEOUS COMMANDS ###
    @commands.command()
    async def shutdown(self, context: commands.Context):
        """turn the bot off from the chat"""
        if context.author.name.lower() != f"{bot.connected_channels[0].name}".lower()\
                or context.author.name.lower() != f"{bot_owner}".lower():
            await context.send(f"You have no power here.")
        else:
            await context.send(f"{bot_owner} wants me gone. Goodbye :(")
            await self.close()

    @commands.cooldown(rate=1, per=5)
    @commands.command(aliases=["songrequest"])
    async def sr(self, context: commands.Context):
        """adds a youtube song to a playlist"""
        try:
            sr_ins = songrequest.Playlist()
            # parse user command to get the youtube link.
            # if they use #sr
            if "#sr" in context.message.content[:3]:
                link = context.message.content[4:]
            # else it must be #songrequest
            else:
                link = context.message.content[13:]
            try:
                playlist_id = await sr_ins.make_playlist()
                await songrequest.song_request(playlist_id, link)
                await context.send(f"{context.author.mention}'s song added to playlist.")
            except Exception as e:
                await context.send("I cannot play that link. Make sure it is a valid YouTube link.")
                print(e)
        except twitchio.ext.commands.errors.CommandOnCooldown as cooldown_error:
            await context.send("Command is on cooldown.")


# instantiate the Bot class
bot = Bot()
