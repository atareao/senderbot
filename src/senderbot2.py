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
    logging.warning('Update "%s" caused error "%s"' % (0, 0))
    custom_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='opcion 1', callback_data='1'),
          InlineKeyboardButton(text='opcion 2', callback_data='2')],
         [InlineKeyboardButton(text='opcion 3', callback_data='3'),
          InlineKeyboardButton(text='opcion 4', callback_data='4')]])
    bot.sendMessage(update.message.chat_id,
                    text='Ejemplo de teclado:',
                    reply_markup=custom_keyboard)


def button(bot, update):
    logging.warning('Update "%s" caused error "%s"' % (1, 1))

    bot.edit_message_text(
        text="Selected option: %s" % update.callback_query.data,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id)


def calculator(bot, update):
    keyboard = [[InlineKeyboardButton("7", callback_data='7'),
                 InlineKeyboardButton("8", callback_data='8'),
                 InlineKeyboardButton("9", callback_data='9'),
                 InlineKeyboardButton("/", callback_data='/')],

                [InlineKeyboardButton("4", callback_data='4'),
                 InlineKeyboardButton("5", callback_data='5'),
                 InlineKeyboardButton("6", callback_data='6'),
                 InlineKeyboardButton("*", callback_data='*')],

                [InlineKeyboardButton("1", callback_data='1'),
                 InlineKeyboardButton("2", callback_data='2'),
                 InlineKeyboardButton("3", callback_data='3'),
                 InlineKeyboardButton("+", callback_data='+')],

                [InlineKeyboardButton("0", callback_data='0'),
                 InlineKeyboardButton(".", callback_data='.'),
                 InlineKeyboardButton("-", callback_data='-'),
                 InlineKeyboardButton("√", callback_data='√')]]

    def CallbackQueryHandler():
        if update.callback_query.data == "7":
            update.message.reply_text("Complete")

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def help(bot, update):
    logging.warning('Update "%s" caused error "%s"' % (2, 2))
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (3, 3))
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
configuration = Configuration()
token = configuration.get('token')
if token is not None and len(token) > 0:
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(callback=button, pattern=None))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(CommandHandler('calculator', calculator))
    updater.dispatcher.add_handler(CommandHandler('7', CallbackQueryHandler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
