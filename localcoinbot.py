from telegram.ext import Updater, CommandHandler
import logging

from settings import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    print(update)
    print(context)
    context.message.reply_text('Hi! My name is LocalCoinBot. How can I be of assistance?')

def admins(update, context):
    admins = update.getChatAdministrators(chat_id=context.effective_chat.id)
    admin_names = [ '@'+i.user.username for i in admins ]
    reply = 'The following users are the ONLY admins in this group. Do not trust anyone else:\n'+'\n'.join(admin_names)
    context.message.reply_text(reply)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Start the bot
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    # Handle /start command
    dispatcher.add_handler(CommandHandler('start', start))
    # Handle /admin command
    dispatcher.add_handler(CommandHandler('admins', admins))
    dispatcher.add_handler(CommandHandler('admin', admins))
    # Error handler
    dispatcher.add_error_handler(error)
    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()