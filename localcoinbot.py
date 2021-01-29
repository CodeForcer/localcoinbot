#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update
import requests
import datetime
from random import shuffle

import messages
import config
from settings import TOKEN
from settings import GROUP_ID

from config import PARAMS
from config import LOGGER
from config import EXCHANGE_URL

GREET_EVERY = 1
WELCOME_COUNTER = 1


def start(update: Update, context: CallbackContext):
    if is_public_chat(update, context):
        context.message.reply_text(
            messages.msg_start, parse_mode=ParseMode.HTML)
    else:
        username = context['message'].from_user.first_name
        chat_id = context['message'].chat.id
        try:
            telegram_unique_token = context['message'].text.split('/start ')[1]
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


def subscribe(update: Update, context: CallbackContext):
    try:
        username = context['message'].from_user.first_name
        chat_id = context['message'].chat.id
        telegram_unique_token = context['message'].text.split('/subscribe ')[1]
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


def error(update: Update, context: CallbackContext):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def admins(update: Update, context: CallbackContext):
    admins = update.getChatAdministrators(chat_id=context.effective_chat.id)
    admin_names = ['@'+i.user.username for i in admins]
    for i in admin_names:
        if ('bot' in i) or ('Bot' in i):
            admin_names.remove(i)
    reply = messages.msg_admins+'\n'.join(admin_names)
    context.message.reply_text(reply, parse_mode=ParseMode.HTML)


def hodor(update: Update, context: CallbackContext):
    try:
        for new_member in update.message.new_chat_members:
            callback_id = str(new_member.id)
            context.bot.restrict_chat_member(
                int(GROUP_ID),
                new_member.id,
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )

            keyboard_items = [
                InlineKeyboardButton("🟢", callback_data=callback_id + ',circle'),
                InlineKeyboardButton("🔷", callback_data=callback_id + ',diamond'),
                InlineKeyboardButton("🟪", callback_data=callback_id + ',square'),
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


            context.bot.sendMessage(
                int(GROUP_ID),
                text=messages.msg_welcome.replace("{{username}}", str(new_member.first_name)),
                parse_mode='HTML',
                reply_markup=reply_markup,
                disable_web_page_preview=True)

    except AttributeError:
        pass


def button(update, context):
    query = update.callback_query
    person_who_pushed_the_button = int(query.data.split(",")[0])
    print("Query user: " + str(query.from_user))
    print("Query data: " + str(query.data))

    if query.from_user.id == person_who_pushed_the_button:
        if 'circle' in query.data:
            context.bot.delete_message(
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id
            )
            context.bot.restrict_chat_member(
                int(GROUP_ID),
                person_who_pushed_the_button,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        else:
            context.bot.delete_message(
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id
                )


def communities(update, context):
    chat_id = context.message.chat.id
    update.sendMessage(
        chat_id=chat_id,
        text=messages.msg_communities,
        parse_mode='HTML',
        disable_web_page_preview=True)


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
    if context.message.chat.type != 'private':
        context.message.reply_text(
            messages.msg_not_private, parse_mode=ParseMode.HTML)
        return False
    else:
        return True


def is_public_chat(update, context):
    if context.message.chat.type != 'supergroup':
        return False
    else:
        return True


def punish(update, context):
    if is_admin(update, context):
        username = context.message.reply_to_message.from_user.username
        banned_until = datetime.datetime.now()+datetime.timedelta(hours=24)
        message = messages.msg_punished.format(username)
        update.restrictChatMember(
            chat_id=context.message.chat.id,
            user_id=context.message.reply_to_message.from_user.id,
            until_date=banned_until)
        context.message.reply_text(message, parse_mode=ParseMode.HTML)


def forgive(update, context):
    if is_admin(update, context):
        username = context.message.reply_to_message.from_user.username
        message = messages.msg_forgiven.format(username)
        update.restrictChatMember(
            chat_id=context.message.chat.id,
            user_id=context.message.reply_to_message.from_user.id,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True)
        context.message.reply_text(message, parse_mode=ParseMode.HTML)


def mute(update, context):
    if is_admin(update, context):
        print('User is admin')  # DEBUG
        dispatcher.add_handler(mute_handler)
    else:
        context.message.reply_text(
            messages.msg_only_admins, parse_mode=ParseMode.HTML)


def unmute(update, context):
    if is_admin(update, context):
        print('User is admin')  # DEBUG
        dispatcher.remove_handler(mute_handler)
    else:
        context.message.reply_text(
            messages.msg_only_admins, parse_mode=ParseMode.HTML)


def debug_group_id(update, context):
    print('GROUP CHAT ID', context.message.chat.id)
    print('CONTEXT', context)
    print('UPDATE', update)


def main():
    # Start the bot
    updater = Updater(str(TOKEN), use_context=True)
    dispatcher = updater.dispatcher

    # Error handler & debug
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler('debug', debug_group_id))

    # Handle /start command
    dispatcher.add_handler(CommandHandler('start', start))

    # Handle /admin command
    dispatcher.add_handler(CommandHandler('admins', admins))
    dispatcher.add_handler(CommandHandler('admin', admins))

    dispatcher.add_handler(MessageHandler(Filters.chat(int(GROUP_ID)), hodor), group=1)
    dispatcher.add_handler(CallbackQueryHandler(button), group=1)

    # Handle communities post
    dispatcher.add_handler(CommandHandler('communities', communities))

    # Mute and unmmute channel
    mute_handler = MessageHandler(Filters.text, delete_all_messages)
    dispatcher.add_handler(CommandHandler('mute', mute))
    dispatcher.add_handler(CommandHandler('unmute', unmute))

    # Restrict a user from posting for 60 seconds
    dispatcher.add_handler(CommandHandler('punish', punish))
    dispatcher.add_handler(CommandHandler('forgive', forgive))

    # Is private chat?
    dispatcher.add_handler(CommandHandler('chat', is_private_chat))

    # Start the bot and run until a kill signal arrives
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
