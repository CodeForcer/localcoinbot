#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatPermissions
from pycoingecko import CoinGeckoAPI
from langid.langid import LanguageIdentifier, model
from random import shuffle, choice
import requests
import time
import json

import messages
import config

from settings import TOKEN
from settings import MYMEMORY_KEY
from settings import MYMEMORY_CONTACT
from settings import EXCHANGE_URL

from config import PARAMS
from config import LOGGER


GREET_EVERY = 1
WELCOME_COUNTER = 1

# How Agressive is the Cleaner (Seconds)
PATIENCE = 60

# Coingecko API Wrapper
cg = CoinGeckoAPI()

# Language Detection
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)


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
        remove_command(context, update)
        bot_hello = context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text=messages.msg_start,
            parse_mode=ParseMode.HTML)

        cleaner(context, bot_hello)
    else:
        username = update.message.from_user.first_name
        chat_id = update.effective_message.chat.id
        try:
            LOGGER.info(f'Subscription token message {update.message.text}')
            telegram_unique_token = update.message.text.split('/start ')[1]
            params = {
                'telegram_unique_token': telegram_unique_token,
                'chat_id': chat_id
            }
            x = requests.post(EXCHANGE_URL, data=params)
            LOGGER.info(f'Subscription response {x.status_code} {x.text}')
            if x.status_code == 200:
                message = messages.msg_subscribe.format(username, chat_id)
                context.bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
            else:
                message = messages.msg_subscribe_error
                context.bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
        except Exception as e:
            message = messages.msg_default_start.format(username)
            context.bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)
            LOGGER.warning(f'<start> Exception Occured: {str(e)}')


def subscribe(update, context):
    try:
        username = update.message.from_user.first_name
        chat_id = update.effective_message.chat.id
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
        LOGGER.warning(f'<subscribe> Exception Occured: {str(e)}')


def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def admins(update, context):
    admins = context.bot.getChatAdministrators(chat_id=update.effective_message.chat.id)
    admin_names = ['@'+i.user.username for i in admins]
    for i in admin_names:
        if ('bot' in i) or ('Bot' in i):
            admin_names.remove(i)
    reply = messages.msg_admins+'\n'.join(admin_names)
    admin_msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat.id,
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
        LOGGER.warning(f'<delete_bot_message> Exception Occured: {str(e)}')
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
                chat_id=update.effective_message.chat.id,
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

            random_item = choice(keyboard_items)

            counter = 0
            for i in range(1):  # create a list with nested lists
                keyboard.append([])
                for n in range(3):
                    keyboard_item = keyboard_items[counter]
                    keyboard[i].append(keyboard_item)  # fills nested lists with data
                    counter += 1

            reply_markup = InlineKeyboardMarkup(keyboard)
            hi_there = messages.msg_welcome.format(
                str(new_member.first_name),
                random_item["text"]
                )

            welcome_message = context.bot.sendMessage(
                chat_id=update.effective_message.chat.id,
                text=hi_there,
                parse_mode='HTML',
                reply_markup=reply_markup,
                disable_web_page_preview=True)

            cleaner(context, welcome_message)

    except AttributeError:
        pass


def button(update, context):
    query = update.callback_query
    person_who_pushed_the_button = int(query.data.split(",")[0])

    if "🟢" in query.message.text:
        query_item = "circle"
    elif "🔶" in query.message.text:
        query_item = "diamond"
    else:
        query_item = "square"

    if query.from_user.id == person_who_pushed_the_button:
        if query_item in query.data:
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
    remove_command(context, update)
    community_msg = context.bot.sendMessage(
        chat_id=update.effective_message.chat.id,
        text=messages.msg_communities,
        parse_mode='HTML',
        disable_web_page_preview=True)
    cleaner(context, community_msg)


def delete_all_messages(update, context):
    update.deleteMessage(
        chat_id=update.effective_message.chat.id,
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
            chat_id=update.effective_message.chat.id,
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
    remove_command(context, update)
    contract_msg = context.bot.sendMessage(
        chat_id=update.effective_message.chat.id,
        text=messages.msg_contract,
        parse_mode='HTML',
        disable_web_page_preview=True)
    cleaner(context, contract_msg)


def exchanges(update, context):
    remove_command(context, update)
    exchange_msg = context.bot.sendMessage(
        chat_id=update.effective_message.chat.id,
        text=messages.msg_exchanges,
        parse_mode='HTML',
        disable_web_page_preview=True)
    cleaner(context, exchange_msg)


def support(update, context):
    remove_command(context, update)
    support_link = context.bot.sendMessage(
        chat_id=update.effective_message.chat.id,
        text=messages.msg_help,
        parse_mode='HTML',
        disable_web_page_preview=True)
    cleaner(context, support_link)


def socials(update, context):
    remove_command(context, update)
    socials_msg = context.bot.sendMessage(
        chat_id=update.effective_message.chat.id,
        text=messages.msg_socials,
        parse_mode='HTML',
        disable_web_page_preview=True)
    cleaner(context, socials_msg)


def gas(update, context):
    # Show Current Estimates for Gas prices
    remove_command(context, update)
    try:
        resp = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
        if resp.status_code == 200:
            prices = resp.json()

            low = prices['result']['SafeGasPrice']
            standard = prices['result']['ProposeGasPrice']
            fast = prices['result']['FastGasPrice']

            message = messages.msg_gas.format(fast, standard, low)

            gas_msg = context.bot.send_message(
                chat_id=update.effective_message.chat.id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
                )
            cleaner(context, gas_msg)

    except TypeError as e:
        LOGGER.warning(f'Rate Limited - {str(e)}')
        message = "Sorry Unable to Fetch Gas Estimates Right Now..."
        gas_message = context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text=message,
            parse_mode=ParseMode.HTML
            )
        cleaner(context, gas_message)


def price(update, context):
    # Gather and Show Crypto Stats
    remove_command(context, update)
    price_resp = cg.get_price(
        ids=context.args[0],
        vs_currencies=context.args[1],
        include_market_cap='true',
        include_24hr_vol='true',
        include_24hr_change='true',
        )

    base_pair = str(context.args[1]).upper()
    crypto = str(context.args[0]).upper()

    try:
        crypto_stats = price_resp.get(context.args[0])

        # Cap Decimals Places at 2 Unless Token Price is Less than 1
        full_price = price_resp.get(context.args[0]).get(context.args[1])
        if int(full_price) < 1:
            only_price = full_price
        else:
            only_price = f'{price_resp.get(context.args[0]).get(context.args[1]):,.2f}'

        market_cap = f"{crypto_stats.get('usd_market_cap'):,.2f} {base_pair}"
        volume = f"{crypto_stats.get('usd_24h_vol'):,.2f} {base_pair}"
        daily_change = f"{crypto_stats.get('usd_24h_change'):,.2f}%"

        price_msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat.id,
            text=messages.msg_crypto_stats.format(
                crypto,
                base_pair,
                only_price,
                base_pair,
                volume,
                market_cap,
                daily_change),
            parse_mode='HTML',
            disable_web_page_preview=True)

    except:
            # Assume Price Check Failed if Price is None
            try:
                only_price = price_resp.get(context.args[0]).get(context.args[1])
                if only_price is None:
                    raise AttributeError

                # Remove Notation from Long Floats
                if int(only_price) == 0:
                    only_price = f'{only_price:18f}'

                price_msg = context.bot.sendMessage(
                    chat_id=update.effective_message.chat.id,
                    text=messages.msg_stats_price.format(
                        crypto,
                        base_pair,
                        only_price,
                        base_pair),
                    parse_mode='HTML',
                    disable_web_page_preview=True)

            except AttributeError:
                price_msg = context.bot.sendMessage(
                chat_id=update.effective_message.chat.id,
                text=messages.msg_stats_fail,
                parse_mode='HTML',
                )

    cleaner(context, price_msg)


def remove_command(context, update):
    # Delete Bot Commands from Group Members
    msg = update.effective_message
    try:
        msg.delete()
        LOGGER.info(f'CMD Message Deleted - {msg.message_id}')
    except BaseException as e:
        LOGGER.info(f'CMD Message Already Deleted - {str(e)}')


def unknown_command(context, update):
    # Delete Unknown Bot Commands from Group Members
    msg = context.effective_message

    try:
        msg.delete()
        LOGGER.info(f'CMD Message Deleted - {msg.message_id}')
    except BaseException as e:
        LOGGER.info(f'CMD Message Already Deleted - {str(e)}')


def translate(context, update):
    # Checks if Language is English, if Confident it isn't Translate & Reply
    msg_text = context.effective_message.text
    lang, confidence = identifier.classify(msg_text)

    if lang != "en" and confidence >= 0.9:
        try:
            # Create Langpair to Show Translation API What We Need
            langpair = lang + '|en'

            translated_msg = requests.get(
                'https://api.mymemory.translated.net/get',
                params={
                    'q': msg_text,
                    'key': MYMEMORY_KEY, # API Key
                    'langpair': langpair,
                    'de': MYMEMORY_CONTACT # Contact Email
                    }).json()

            # Grab Translated Text from Nested JSON Response
            final_translation = translated_msg['matches'][0]['translation']

            # Respond with Translation to Non-English Message
            context.effective_message.reply_text(
                messages.msg_translate.format(final_translation),
                parse_mode='HTML')
        except Exception as e:
            LOGGER.warning(f'Translation Failed - {str(e)}')


def translate_request(update, context):
    remove_command(context, update)

    # Make Sure it's a Public Chat
    if is_public_chat(update, context) is False:
        context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text="It's only us here, I won't do that")
        return

    try:
        # Check that the User Actually Replied to a Message
        replied_message = update.message.reply_to_message.text

    except AttributeError:
                context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text="You didn't reply to a message...",)
                return

    try:
        lang, confidence = identifier.classify(replied_message)

        if context.args[0] == "en":
            langpair = lang + '|en'
        else:
            langpair = 'en|' + context.args[0]

    except IndexError:
        # If No Language is Provided Assume Goal is English
        lang, confidence = identifier.classify(replied_message)
        if lang == "en":
            context.bot.send_message(
                    chat_id=update.effective_message.chat.id,
                    text="Message already appears to be English, unsure what to do.")
            return
        else:
            langpair = lang + '|en'

    try:
        translated_msg = requests.get(
            'https://api.mymemory.translated.net/get',
            params={
                'q': replied_message,
                'key': MYMEMORY_KEY, # API Key
                'langpair': langpair,
                'de': MYMEMORY_CONTACT # Contact Email
                }).json()

        # Grab Translated Text from Nested JSON Response
        final_translation = translated_msg['matches'][0]['translation']

        # Respond with Translation to Non-English Message
        context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text=messages.msg_translate.format(final_translation),
            parse_mode='HTML')

    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_message.chat.id,
            text=messages.msg_translate_failed,
            parse_mode='HTML')

        LOGGER.info(f'Translation Failed - {str(e)}')


def main():
    # Start the bot
    updater = Updater(str(TOKEN))
    dp = updater.dispatcher

    # Error handler & debug
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('debug', debug_group_id, run_async=True))

    # Handle /start command
    dp.add_handler(CommandHandler('start', start, run_async=True))

    # Handle /admin command
    dp.add_handler(CommandHandler('admins', admins, run_async=True))
    dp.add_handler(CommandHandler('admin', admins, run_async=True))

    dp.add_handler(MessageHandler(Filters.chat_type.supergroup, hodor, run_async=True), group=1)
    dp.add_handler(CallbackQueryHandler(button, run_async=True), group=1)

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
    dp.add_handler(CommandHandler('support', support, run_async=True))

    # Show Links to Socials
    dp.add_handler(CommandHandler('socials', socials, run_async=True))

    # Estimate Gas Prices
    dp.add_handler(CommandHandler('gas', gas, run_async=True))

    dp.add_handler(CommandHandler('private', is_private_chat, run_async=True))

    # Fetch Crypto Stats
    dp.add_handler(CommandHandler('price', price, run_async=True))

    # Manual Translation Requests
    dp.add_handler(CommandHandler('translate', translate_request, run_async=True))

    # Delete Unknown Command Messages from Group Members
    dp.add_handler(MessageHandler(Filters.command, unknown_command, run_async=True))

    # Translate Non-English Messages
    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.supergroup & ~Filters.command, translate, run_async=True))

    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
