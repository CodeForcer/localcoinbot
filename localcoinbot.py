#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ParseMode
import requests
import datetime
import csv

from settings import TOKEN
from messages import (
    msg_start,
    msg_admins,
    msg_price,
    msg_price_error,
    msg_welcome,
    msg_communities,
    msg_not_private,
    msg_not_supergroup,
    msg_punished,
    msg_forgiven,
    msg_promo_intro,
    msg_promo_email_prompt,
    msg_promo_email_given,
    msg_promo_twitter_prompt,
    msg_promo_twitter_given,
    msg_promo_trade_prompt,
    msg_promo_trade_given,
    msg_promo_complete,
    msg_only_admins,
)
from config import (
    PROMO_FIVE_FILE,
    EMAIL,
    TWITTER,
    CONTRACT,
    URL,
    HEADERS,
    PARAMS,
    LOGGER,
)

def start(update, context):
    print(update, context) # DEBUG
    context.message.reply_text(msg_start, parse_mode=ParseMode.HTML)

def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)

def admins(update, context):
    admins = update.getChatAdministrators(chat_id=context.effective_chat.id)
    admin_names = [ '@'+i.user.username for i in admins ]
    reply = msg_admins+'\n'.join(admin_names)
    context.message.reply_text(reply, parse_mode=ParseMode.HTML)

def price(update, context):
    if is_public_chat(update, context):
        response = requests.get(URL, params=PARAMS, headers=HEADERS)
        if response.status_code == 200:
            price = response.json()['data']['LCS']['quote']['USD']['price']
            change = '{}%'.format(response.json()['data']['LCS']['quote']['USD']['percent_change_24h'])
            output = msg_price.format(price, change)
        else:
            output = msg_price_error
        context.message.reply_text(output, parse_mode=ParseMode.HTML) 

def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
        new_user = ""
        try:
            new_user = new_user_obj['username']
        except Exception as e:
            new_user = new_user_obj['first_name']
        bot.sendMessage(chat_id=update.message.chat.id, text=msg_welcome.replace("{{username}}",str(new_user)), parse_mode='HTML')

def communities(update, context):
    chat_id = context.message.chat.id
    update.sendMessage(chat_id=chat_id, text=msg_communities, parse_mode='HTML', disable_web_page_preview=True)

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
        context.message.reply_text(msg_not_private, parse_mode=ParseMode.HTML)
        return False
    else:
        return True

def is_public_chat(update, context):
    if context.message.chat.type != 'supergroup':
        context.message.reply_text(msg_not_supergroup, parse_mode=ParseMode.HTML)
        return False
    else:
        return True

def punish(update, context):
    if is_admin(update, context) == True:
        username = context.message.reply_to_message.from_user.username
        banned_until = datetime.datetime.now()+datetime.timedelta(hours=24)
        message = msg_punished.format(username)
        update.restrictChatMember(chat_id=context.message.chat.id, user_id=context.message.reply_to_message.from_user.id, until_date=banned_until)
        context.message.reply_text(message, parse_mode=ParseMode.HTML)

def forgive(update, context):
    if is_admin(update, context) == True:
        username = context.message.reply_to_message.from_user.username
        message = msg_forgiven.format(username)
        update.restrictChatMember(chat_id=context.message.chat.id, user_id=context.message.reply_to_message.from_user.id,can_send_messages=True,can_send_media_messages=True,can_send_other_messages=True,can_add_web_page_previews=True)
        context.message.reply_text(message, parse_mode=ParseMode.HTML)

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
        return ConversationHandler.END
    else:
        context.message.reply_text(msg_promo_intro, parse_mode=ParseMode.HTML)
        context.message.reply_text(msg_promo_email_prompt, parse_mode=ParseMode.HTML)
        return EMAIL

def one_email(update, context, user_data):
    text = context.message.text
    user_data['email'] = text
    context.message.reply_text(msg_promo_email_given.format(text.lower()), parse_mode=ParseMode.HTML)
    context.message.reply_text(msg_promo_twitter_prompt, parse_mode=ParseMode.HTML)
    return TWITTER

def two_twitter(update, context, user_data):  
    text = context.message.text
    user_data['twitter'] = text
    context.message.reply_text(msg_promo_twitter_given.format(text.lower()), parse_mode=ParseMode.HTML)
    context.message.reply_text(msg_promo_trade_prompt, parse_mode=ParseMode.HTML)
    return CONTRACT

def three_contract(update, context, user_data):
    text = context.message.text
    user_data['trade'] = text
    context.message.reply_text(msg_promo_trade_given.format(text.lower()), parse_mode=ParseMode.HTML)
    context.message.reply_text(msg_promo_complete.format(facts_to_str(user_data)), parse_mode=ParseMode.HTML)
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
            context.message.reply_text(msg_only_admins, parse_mode=ParseMode.HTML)
    def unmute(update, context):
        if is_admin(update, context) == True:
            print('User is admin') # DEBUG
            dispatcher.remove_handler(mute_handler)
        else:
            context.message.reply_text(msg_only_admins, parse_mode=ParseMode.HTML)
    mute_handler = MessageHandler(Filters.text, delete_all_messages)
    dispatcher.add_handler(CommandHandler('mute', mute))
    dispatcher.add_handler(CommandHandler('unmute', unmute))
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