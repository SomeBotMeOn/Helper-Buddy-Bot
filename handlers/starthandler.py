# Для обработки команды старт
from gc import callbacks
import sqlite3
import telebot
import requests
from telebot import types

from bot_instance import bot
from utilits.assets import stickers, emoji
from handlers.messagehandler_2 import user_name, callback
from bot_instance import bot
from handlers.messagehandler_2 import buttons


def main(message):
    # Хранит информацию про пользователя и чат
    first_name = message.from_user.first_name if message.from_user.first_name else 'Незнакомец'
    last_name = message.from_user.last_name if message.from_user.last_name else ''

    greeting_message = (f'<b>Привет, {first_name} {last_name}!</b>\n'
                        'Я телеграм-бот, который может помочь Вам узнать '
                        'погоду в данный момент и как она ощущается лично для Вас, '
                        'а также определиться куда сегодня пойти.')
    bot.send_message(message.chat.id, greeting_message, parse_mode='html')

    ask_name_message = 'Как я могу к Вам обращаться?'
    bot.send_message(message.chat.id, ask_name_message, parse_mode='html')

    bot.register_next_step_handler(message, user_name)

    #  ПЕРЕСТАВИТЬ GREETING MESSAGE В USER_NAME
