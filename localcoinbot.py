from telegram.ext import Updater, CommandHandler
import logging
import requests

from settings import TOKEN, API_KEY

CMC_CLIENT_CONFIG = {
    'host': 'https://pro-api.coinmarketcap.com/',
    'version': 'v1/',
}
url = CMC_CLIENT_CONFIG['host'] + CMC_CLIENT_CONFIG['version'] + 'cryptocurrency/quotes/latest'
headers = {
    'X-CMC_PRO_API_KEY': API_KEY
    }
get_params = {
        'symbol': 'LCS'
    }

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    # print(update, context) # DEBUG
    context.message.reply_text('Hi! My name is LocalCoinBot. How can I be of assistance?')

def admins(update, context):
    admins = update.getChatAdministrators(chat_id=context.effective_chat.id)
    admin_names = [ '@'+i.user.username for i in admins ]
    reply = 'The following users are the ONLY admins in this group. Do not trust anyone else:\n'+'\n'.join(admin_names)
    context.message.reply_text(reply)

def price(update, context):
    response = requests.get(url, params=get_params, headers=headers)
    if response.status_code == 200:
        price = response.json()['data']['LCS']['quote']['USD']['price']
        change = '{}%'.format(response.json()['data']['LCS']['quote']['USD']['percent_change_24h'])
        output = 'The current price of LCS in USD value is: {}\n\nIn the last 24 hours the price has changed: {}'.format(price, change)
    else:
        output = 'I was unable to grab the latest price data'
    context.message.reply_text(output) 

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
    # Grab prices with /price command
    dispatcher.add_handler(CommandHandler('price', price))
    # Error handler
    dispatcher.add_error_handler(error)
    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()