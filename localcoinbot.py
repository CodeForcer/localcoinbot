#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from emoji import emojize
import logging
import requests
import datetime
import csv

from settings import TOKEN, API_KEY

PROMO_FIVE_FILE = 'PROMO5.CSV'
EMAIL, TWITTER, CONTRACT = range(3)
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
    context.message.reply_text(emojize('Hi! My name is LocalCoinBot. I\'m already started :smiley:', use_aliases=True))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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
    def get_admin_ids(bot, chat_id):
        return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
    if context.message.from_user.id in get_admin_ids(update, context.message.chat_id):
        return True
    else:
        return False

def is_private_chat(update, context):
    if context.message.chat.type != 'private':
        context.message.reply_text(emojize('I\'m feeling a little shy, and this isn\'t a good place to chat :sweat: Message me privately so we can get better acquainted', use_aliases=True))
        return False
    else:
        return True

def punish(update, context):
    if is_admin(update, context) == True:
        username = context.message.reply_to_message.from_user.username
        banned_until = datetime.datetime.now()+datetime.timedelta(hours=24)
        message = '{} has been a very naughty meat-sack. I\'m going to put them in timeout for 24 hours'.format(username)
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

#### PROMO FUNCTIONS ####

def facts_to_str(user_data):
    facts = list()
    for key, value in user_data.items():
        facts.append('{}: {}'.format(key, value))
    return "\n".join(facts).join(['\n', '\n'])

def append_to_csv(telegram_username, email, twitter, trade, file=PROMO_FIVE_FILE):
    fields=[telegram_username,email,twitter,trade]
    with open(file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def promo_five(update, context):
    if not is_private_chat(update, context):
        return False
    else:
        context.message.reply_text('Thank you for taking part in our promotion, please answer a couple of short questions to register your details')
        context.message.reply_text('What is your email address which you used on the LocalCoinSwap exchange?')
        return EMAIL

def one_email(update, context, user_data):
    text = context.message.text
    user_data['email'] = text
    context.message.reply_text(
        'Your email address is {}? Great, lets continue!'.format(text.lower()))
    context.message.reply_text('What is your Twitter address you are Tweeting about LocalCoinSwap from?')
    return TWITTER

def two_twitter(update, context, user_data):  
    text = context.message.text
    user_data['twitter'] = text
    context.message.reply_text(
        'Your Twitter address is {}? Great, lets continue!'.format(text.lower()))
    context.message.reply_text('What is your url for the completed trade you wish to claim a prize for?')
    return CONTRACT

def three_contract(update, context, user_data):
    text = context.message.text
    user_data['trade'] = text
    context.message.reply_text(
        'Your trade url is {}? Great!'.format(text.lower()))
    context.message.reply_text("The following details have been entered into our promotion:"
                              "{}"
                              "It normally takes 5-7 days for prizes to be allocated. Thanks for your participation!".format(facts_to_str(user_data)))
    user = context.message.from_user.username
    append_to_csv(telegram_username=user, email=user_data['email'], twitter=user_data['twitter'], trade=user_data['trade'])
    user_data.clear()
    return ConversationHandler.END

###########################

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
    # Promo code functionality
    promo_handler = ConversationHandler(
        entry_points=[CommandHandler('promo5', promo_five)],
        states={
            EMAIL: [MessageHandler(Filters.text, one_email, pass_user_data=True),],
            TWITTER: [MessageHandler(Filters.text, two_twitter, pass_user_data=True),],
            CONTRACT: [MessageHandler(Filters.text, three_contract, pass_user_data=True),],
        },
        fallbacks=[None]
    )
    dispatcher.add_handler(promo_handler)
    # Is private chat?
    dispatcher.add_handler(CommandHandler('chat', is_private_chat))
    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()