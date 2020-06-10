#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler
from telegram import ParseMode
import requests
import datetime
import csv

import messages
import config
from settings import TOKEN

from config import PARAMS
from config import LOGGER
from config import EXCHANGE_URL


def start(update, context):
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


def subscribe(update, context):
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


def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def admins(update, context):
    admins = update.getChatAdministrators(chat_id=context.effective_chat.id)
    admin_names = ['@'+i.user.username for i in admins]
    for i in admin_names:
        if ('bot' in i) or ('Bot' in i):
            admin_names.remove(i)
    reply = messages.msg_admins+'\n'.join(admin_names)
    context.message.reply_text(reply, parse_mode=ParseMode.HTML)


def welcome(bot, update):
    for new_user_obj in update.message.new_chat_members:
        new_user = ""
        try:
            new_user = new_user_obj['name']
        except Exception as e:
            new_user = new_user_obj['first_name']
        bot.sendMessage(
            chat_id=update.message.chat.id,
            text=messages.msg_welcome.replace("{{username}}", str(new_user)),
            parse_mode='HTML')


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


def play_welcome(update, context):
    context.message.reply_text(messages.msg_welcome, parse_mode=ParseMode.HTML)


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
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # Error handler & debug
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(CommandHandler('debug', debug_group_id))

    # Handle /start command
    dispatcher.add_handler(CommandHandler('start', start))

    # Handle /admin command
    dispatcher.add_handler(CommandHandler('admins', admins))
    dispatcher.add_handler(CommandHandler('admin', admins))

    # Handle welcome
    dispatcher.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome))
    dispatcher.add_handler(CommandHandler('greet', play_welcome))

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
