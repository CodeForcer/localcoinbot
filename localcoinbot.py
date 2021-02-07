#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatPermissions

import requests
import datetime
from random import shuffle

import time
import messages
import config
from settings import TOKEN

from config import PARAMS
from config import LOGGER
from config import EXCHANGE_URL

GREET_EVERY = 1
WELCOME_COUNTER = 1

# How Agressive is the Cleaner (Seconds)
PATIENCE = 60


def good_permissions():
    return ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
    )

def bad_permissions():
    return ChatPermissions(None)


def start(update, context):
    if is_public_chat(update, context):
        bot_hello = context.bot.send_message(
            chat_id=update.message.chat.id,
            text=messages.msg_start,
            parse_mode=ParseMode.HTML)

        cleaner(context, bot_hello)
    else:
            username = update.message.from_user.first_name
            chat_id = update.message.chat.id
            try:
                telegram_unique_token = update.message.text.split('/start ')[1]
                params = {
                    'telegram_unique_token': telegram_unique_token,
                    'chat_id': chat_id
                }
                x = requests.post(EXCHANGE_URL, data=params)
                if x.status_code == 200:
                    message = messages.msg_subscribe.format(username, chat_id)
                    context.message.reply_text(message, parse_mode=ParseMode.HTML)
                else:
                    message = messages.msg_subscribe_error
                    context.bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
            except Exception as e:
                message = messages.msg_default_start.format(username)
                context.bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
                LOGGER.warning(f'Exception Occured: {str(e)}')


def subscribe(update, context):
    try:
        username = update.message.from_user.first_name
        chat_id = update.message.chat.id
        telegram_unique_token = update.message.text.split('/subscribe ')[1]
        params = {
            'telegram_unique_token': telegram_unique_token,
            'chat_id': chat_id
        }
        x = requests.post(EXCHANGE_URL, data=params)
        if x.status_code == 200:
            message = messages.msg_subscribe.format(username, chat_id)
            context.message.reply_text(message, parse_mode=ParseMode.HTML)
        else:
            message = messages.msg_subscribe_error
            context.message.reply_text(message, parse_mode=ParseMode.HTML)
    except Exception as e:
        message = messages.msg_default_start.format(username)
        context.message.reply_text(message, parse_mode=ParseMode.HTML)


def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def admins(update, context):
    admins = context.bot.getChatAdministrators(chat_id=update.message.chat.id)
    admin_names = ['@'+i.user.username for i in admins]
    for i in admin_names:
        if ('bot' in i) or ('Bot' in i):
            admin_names.remove(i)
    reply = messages.msg_admins+'\n'.join(admin_names)
    admin_msg = context.bot.sendMessage(
            chat_id=update.message.chat.id,
            text=reply,
            parse_mode='HTML',
            )

    cleaner(context, admin_msg)

def delete_bot_message(update, context):
    try:
        context.bot.deleteMessage(
            chat_id=update.effective_message.chat.id,
            message_id=update.effective_message.message_id
        )
    except BaseException as e:
        LOGGER.warning(f'Exception Occured: {str(e)}')
        pass


def cleaner(context, message):
    time.sleep(PATIENCE)
    try:
        context.bot.deleteMessage(
            chat_id=message.chat_id,
            message_id=message.message_id
        )
        LOGGER.info(f'Message Deleted - #{message.message_id}')
    except BaseException as e:
        LOGGER.info(f'Message Already Deleted - {str(e)}')
        pass


def hodor(update, context):
    try:
        for new_member in update.message.new_chat_members:
            callback_id = str(new_member.id)
            context.bot.restrictChatMember(
                chat_id=update.message.chat.id,
                user_id=new_member.id,
                permissions=bad_permissions()
            )

            keyboard_items = [
                InlineKeyboardButton("🟢", callback_data=callback_id + ',circle'),
                InlineKeyboardButton("🔶", callback_data=callback_id + ',diamond'),
                InlineKeyboardButton("🟦", callback_data=callback_id + ',square'),
                ]

            shuffle(keyboard_items)
            keyboard = []

            counter = 0
            for i in range(1):  # create a list with nested lists
                keyboard.append([])
                for n in range(3):
                    keyboard_item = keyboard_items[counter]
                    keyboard[i].append(keyboard_item)  # fills nested lists with data
                    counter += 1

            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_message = context.bot.sendMessage(
                chat_id=update.message.chat.id,
                text=messages.msg_welcome.replace("{{username}}", str(new_member.first_name)),
                parse_mode='HTML',
                reply_markup=reply_markup,
                disable_web_page_preview=True)

            cleaner(context, welcome_message)

    except AttributeError:
        pass


def button(update, context):
    query = update.callback_query
    person_who_pushed_the_button = int(query.data.split(",")[0])

    if query.from_user.id == person_who_pushed_the_button:
        if 'circle' in query.data:
            delete_bot_message(update, context)
            context.bot.restrictChatMember(
                chat_id=query.message.chat.id,
                user_id=person_who_pushed_the_button,
                permissions=good_permissions()
            )
        else:
            delete_bot_message(update, context)

        return context


def communities(update, context):
    community_msg = context.bot.sendMessage(
        chat_id=update.message.chat.id,
        text=messages.msg_communities,
        parse_mode='HTML',
        disable_web_page_preview=True)

    cleaner(context, community_msg)


def delete_all_messages(update, context):
    update.deleteMessage(
        chat_id=context.message.chat.id,
        message_id=context.message.message_id)


def is_admin(update, context):
    def get_admin_ids(bot, chat_id):
        return [
            admin.user.id for admin in bot.get_chat_administrators(chat_id)]
    if (context.message.from_user.id in
            get_admin_ids(update, context.message.chat_id)):
        return True
    else:
        return False


def is_private_chat(update, context):
    msg = update.effective_message
    if msg.chat.type != 'private':
        context.bot.sendMessage(
            chat_id=context.message.chat.id,
            text=messages.msg_not_private,
            parse_mode=ParseMode.HTML)
        return False
    else:
        return True


def is_public_chat(update, context):
    msg = update.effective_message
    if msg.chat.type != 'supergroup':
        return False
    else:
        return True


def debug_group_id(update, context):
    print('GROUP CHAT ID', context.message.chat.id)
    print('CONTEXT', context)
    print('UPDATE', update)


def contract(update, context):
    contract_msg = context.bot.sendMessage(
        chat_id=update.message.chat.id,
        text=messages.msg_contract,
        parse_mode='HTML',
        disable_web_page_preview=True)

    cleaner(context, contract_msg)


def exchanges(update, context):
    exchange_msg = context.bot.sendMessage(
        chat_id=update.message.chat.id,
        text=messages.msg_exchanges,
        parse_mode='HTML',
        disable_web_page_preview=True)

    cleaner(context, exchange_msg)


def support(update, context):
    support_link = context.bot.sendMessage(
        chat_id=update.message.chat.id,
        text=messages.msg_help,
        parse_mode='HTML',
        disable_web_page_preview=True)

    cleaner(context, support_link)


def socials(update, context):
    socials_msg = context.bot.sendMessage(
        chat_id=update.message.chat.id,
        text=messages.msg_socials,
        parse_mode='HTML',
        disable_web_page_preview=True)

    cleaner(context, socials_msg)


def gas(update, context):
    try:
        resp = requests.get("https://etherchain.org/api/gasPriceOracle")
        if resp.status_code == 200:
            prices = resp.json()

            low = prices['safeLow']
            standard = prices['standard']
            fast = prices['fast']
            fastest = prices['fastest']

            message = messages.msg_price.format(fastest, fast, standard, low)

            gas_msg = context.bot.send_message(
                chat_id=update.message.chat.id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
                )
            cleaner(context, gas_msg)

        else:
            message = "Sorry Unable to Fetch Gas Estimates Right Now..."
            gas_msg = context.bot.send_message(message, parse_mode=ParseMode.HTML)
            cleaner(context, gas_msg)

    except Exception as e:
        LOGGER.warning(f'Exception Occured: {str(e)}')


def main():
    # Start the bot
    updater = Updater(str(TOKEN))
    dp = updater.dispatcher

    # Error handler & debug
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('debug', debug_group_id))

    # Handle /start command
    dp.add_handler(CommandHandler('start', start))

    # Handle /admin command
    dp.add_handler(CommandHandler('admins', admins, run_async=True))
    dp.add_handler(CommandHandler('admin', admins, run_async=True))

    dp.add_handler(MessageHandler(Filters.chat_type.supergroup, hodor, run_async=True), group=1)
    dp.add_handler(CallbackQueryHandler(button), group=1)

    # Handle communities post
    dp.add_handler(CommandHandler('communities', communities, run_async=True))

    # Is private chat?
    dp.add_handler(CommandHandler('chat', is_private_chat, run_async=True))

    # Provide Link to Token Smart Contract on Etherscan
    dp.add_handler(CommandHandler('contract', contract, run_async=True))

    # List Places to Trade LCS Tokens
    dp.add_handler(CommandHandler('exchanges', exchanges, run_async=True))

    # Show Link to Support Portal
    dp.add_handler(CommandHandler('help', support, run_async=True))

    # Show Links to Socials
    dp.add_handler(CommandHandler('socials', socials, run_async=True))

    # Estimate Gas Prices
    dp.add_handler(CommandHandler('gas', gas, run_async=True))

    dp.add_handler(CommandHandler('private', is_private_chat, run_async=True))

    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
