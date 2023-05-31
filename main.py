import my_routines
import my_bot
from twitchio.ext import commands

# Start the reminder routines.
my_routines.follow_reminder.start()
my_routines.hydration_reminder.start()

# Start the bot
if __name__ == '__main__':
    my_bot.bot.run()


