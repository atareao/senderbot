#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# raebot.py
#
# This file is part of ---
#
# Copyright (C) 2017
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler


def inline_caps(bot, update):
     query = update.inline_query.query
     if not query:
         return
     results = list()
     results.append(
         InlineQueryResultArticle(
             id=query.upper(),
             title='Caps',
             input_message_content=InputTextMessageContent(query.upper())
         )
     )
     bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)