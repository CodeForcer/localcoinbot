from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import datetime

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
    print(update, context) # DEBUG
    context.message.reply_text('Hi! My name is LocalCoinBot. How can I be of assistance?')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]

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

def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
        new_user = ""
        WELCOME_MESSAGE = '<b>Welcome {{username}}!</b>\nYou can start trading 21+ cryptocurrencies, with 250+ payment methods, at <a href="https://localcoinswap.com/">LocalCoinSwap.Com</a>. Signup is instant with no KYC.\nFor any other questions, or just to chat with the community, this group is the place to be.\nPS: Read the pinned post to avoid scammers!'
        try:
            new_user = new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name']
        bot.sendMessage(chat_id=update.message.chat.id, text=WELCOME_MESSAGE.replace("{{username}}",str(new_user)), parse_mode='HTML')

def communities(update, context):
    reply = '<b>--- LocalCoinSwap.Com Official Communities ---</b>\n<a href="https://localcoinswap.com/">LocalCoinSwap Exchange</a>\n<a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>'
    chat_id = context.message.chat.id
    update.sendMessage(chat_id=chat_id, text=reply, parse_mode='HTML')

def delete_all_messages(update, context):
    update.deleteMessage(chat_id=context.message.chat.id, message_id=context.message.message_id)

def is_admin(update, context):
    if context.message.from_user.id in get_admin_ids(update, context.message.chat_id):
        return True
    else:
        return False

def punish(update, context):
    if is_admin(update, context) == True:
        username = context.message.reply_to_message.from_user.username
        banned_until = datetime.datetime.now()+datetime.timedelta(seconds=60)
        message = '{} has been a very naughty meat-sack. I\'m going to put them in timeout for 60 seconds'.format(username)
        update.restrictChatMember(chat_id=context.message.chat.id, user_id=context.message.reply_to_message.from_user.id, until_date=banned_until)
        context.message.reply_text(message)

def forgive(update, context):
    if is_admin(update, context) == True:
        username = context.message.reply_to_message.from_user.username
        message = '{} your sins have been forgiven. Thanks to the mercy of the LocalCoinSwap team your posting rights are unrestricted'.format(username)
        update.restrictChatMember(chat_id=context.message.chat.id, user_id=context.message.reply_to_message.from_user.id,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
        context.message.reply_text(message)

def get_user_id(update, context):
    username = context.message.reply_to_message.from_user.username
    user_id = context.message.reply_to_message.from_user.id
    context.message.reply_text('The person you replied to was {} and their user id is {}'.format(username, user_id))

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
    # Handle welcome
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    # Handle communities post
    dispatcher.add_handler(CommandHandler('communities', communities))
    # Error handler
    dispatcher.add_error_handler(error)
    # Mute and unmmute channel
    def mute(update, context):
        if is_admin(update, context) == True:
            print('User is admin') # DEBUG
            dispatcher.add_handler(mute_handler)
        else:
            context.message.reply_text('Sorry meat-sack, only admins can do this')
    def unmute(update, context):
        if is_admin(update, context) == True:
            print('User is admin') # DEBUG
            dispatcher.remove_handler(mute_handler)
        else:
            context.message.reply_text('Sorry meat-sack, only admins can do this')
    mute_handler = MessageHandler(Filters.text, delete_all_messages)
    dispatcher.add_handler(CommandHandler('mute', mute))
    dispatcher.add_handler(CommandHandler('unmute', unmute))
    # Find out the user ID of a poster we replied to
    dispatcher.add_handler(CommandHandler('user_id', get_user_id))
    # Restrict a user from posting for 60 seconds
    dispatcher.add_handler(CommandHandler('punish', punish))
    dispatcher.add_handler(CommandHandler('forgive', forgive))
    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()