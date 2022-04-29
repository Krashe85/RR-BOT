from dotenv import load_dotenv

load_dotenv()
import datetime
import os

import pytz
from bot.jobs.send_stock import jon_send_stock


from telegram.ext import Updater, CommandHandler, JobQueue, Dispatcher

from bot.commands import start, create_invite, user_registrate, get_id


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(str(os.getenv('TELEGRAM_TOKEN')))

    # Get the dispatcher to register handlers
    dispatcher: Dispatcher = updater.dispatcher
    scheduler: JobQueue = dispatcher.job_queue

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getid", get_id))
    dispatcher.add_handler(CommandHandler("invite", create_invite))
    dispatcher.add_handler(CommandHandler("reg", user_registrate))
    dispatcher.add_handler(CommandHandler("register", user_registrate))

    time_of_day = (datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=10)).time()
    stocks_job = scheduler.run_daily(callback=jon_send_stock, time=time_of_day, name="Stocks")

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
