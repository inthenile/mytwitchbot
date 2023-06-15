import asyncio
import twitchio
import my_bot
from game.scoreboard import Score

#  list to store users who type the  game word into, and select index 0 to get the first one to type.
list_of_users = []

"""function for the mini game of beep boop (found in my_routines)"""
async def mini_game(response: twitchio.Message):
    if response.content == my_bot.bot.game_word and not response.echo:
        print(f"{my_bot.bot.game_word} received")
        list_of_users.append(response.author.name)

async def check_game_status():
    loop = asyncio.get_running_loop()
    # the seconds to wait for before the timer runs out.
    end = loop.time() + 7.0
    while True:
        await asyncio.sleep(1)
    # check whether there is a winner or not, and change the game_active flag.
    # get the first person to have been added to the list, and declare them the winner.
        if len(list_of_users) >= 1:
            await my_bot.bot.connected_channels[0].send(f"Winner is {list_of_users[0]}")
            # storing the score to a local .json file
            store_score = Score(list_of_users[0])
            await store_score.update_score(1)
            break
        # if no one repeated the bot and the timer ran out
        elif (loop.time() + 1.0) >= end:
            await my_bot.bot.connected_channels[0].send("No winners.")
            break
    my_bot.bot.game_active = False
    # empty the list after each round
    list_of_users.clear()
