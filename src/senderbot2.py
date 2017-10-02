#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import pprint
import json
import codecs
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

APP = 'senderbot'
APPNAME = 'SenderBot'
APPCONF = APP + '.conf'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APPCONF)
PARAMS = {'token': None,
          'channel_id': None}

logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s',
                    filename='/tmp/senderbot.log',
                    filemode='w',
                    level=logging.INFO)


class Configuration(object):
    def __init__(self):
        self.params = PARAMS
        self.read()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError as e:
            print(e)
            self.params[key] = PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        self.params[key] = value

    def reset(self):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        self.params = PARAMS
        self.save()

    def set_defaults(self):
        self.params = PARAMS
        self.save()

    def print_config(self):
        pprint(self.params)

    def read(self):
        try:
            f = codecs.open(CONFIG_FILE, 'r', 'utf-8')
        except IOError as e:
            print(e)
            self.save()
            f = codecs.open(CONFIG_FILE, 'r', 'utf-8')
        try:
            self.params = json.loads(f.read())
        except ValueError as e:
            print(e)
            self.save()
        f.close()

    def save(self):
        f = codecs.open(CONFIG_FILE, 'w', 'utf-8')
        f.write(json.dumps(self.params))
        f.close()


def start(bot, update):
    custom_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='opcion 1', callback_data='1'),
          InlineKeyboardButton(text='opcion 2', callback_data='2')],
         [InlineKeyboardButton(text='opcion 3', callback_data='3'),
          InlineKeyboardButton(text='opcion 4', callback_data='4')]])
    bot.send_message(chat_id=update.message.chat_id,
                     text="Custom Keyboard Test",
                     reply_markup=custom_keyboard)


def button(bot, update):
    query = update.callback_query
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Turning on light ON!")
    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
configuration = Configuration()
token = configuration.get('token')
if token is not None and len(token) > 0:
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(callback=button,
                             pass_user_data=True,
                             pass_chat_data=True))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
