from telegram.ext import Updater, CommandHandler
import logging

from settings import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    context.message.reply_text('Hi!')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Start the bot
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    # Handle /start command
    dispatcher.add_handler(CommandHandler('start', start))
    # Error handler
    dispatcher.add_error_handler(error)
    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()