from twitchio.ext import routines
import my_bot

# Timers can be changed.
@routines.routine(wait_first=True, hours=1)
async def follow_reminder():
    """Reminds the audience to follow the stream"""
    await my_bot.bot.connected_channels[0].send("Enjoying the stream? "
                                                "Make sure to drop a follow!")

@routines.routine(wait_first=True, minutes=45)
async def hydration_reminder():
    """Reminder to drink water"""
    await my_bot.bot.connected_channels[0].send("When did you drink water last? "
                                                "Don't forget to hydrate.")
