import my_routines
import my_bot

# Start the reminder routines.
my_routines.follow_reminder.start()
my_routines.hydration_reminder.start()
my_routines.mini_typing_game.start()


# Start the bot
if __name__ == '__main__':
    my_bot.bot.run()
