# модули которые подключаем с других папок
from handlers.starthandler import main
from handlers.messagehandler import info
from handlers.messagehandler_2 import weather
from handlers.messagehandler_2 import information
from handlers.messagehandler_2 import site_with_weather
from utilits.logger import commands

# Описание папок
# Utilits единственный файл который здесь лежит это
#          logger он перемещает команды В @BotFather (бот в тг), эти команды будут встрроены в бот по умолчанию
#Handlers отвечает за обраблтку сообщений
#           starthandler - обработка сообщений при команде старт
#           messangehandler - обработка сообщений от пользователя
#           messangehandler_2 - обработка запросов от встроенных команд бота
# Config - конфигурация
#           main - тело бота, основной файл запуска бота
#           env - файл с зашифрованными данными

# gitignore будет использоватья при загрузку на гитхаб, для зпрета гитхабу на доступ к некоторым приватным папкам

import webbrowser
import time
from datetime import datetime
import requests

# модули для работы с env
import os
from dotenv import load_dotenv

import telebot

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN')) # ссылаемся на токен в файле evn
API_weather = os.getenv('API_W') # ссылаемся на апишник в файле evn
stickers = {
    'hi_sticker': 'CAACAgIAAxkBAAEM2SNm7rivIR7mxs0IVtV7czfYY_hCywACBQADwDZPE_lqX5qCa011NgQ'
}

emoji = {
    'hi_emoji': '\U0001f44b'
}

# обработка команды старт; команда в папке handlers в starthandler
@bot.message_handler(commands=['start'])
def start_handler(message):
    main(message)

# обработка других встроенных команд бота, всё с файла messagehandler_2
@bot.message_handler(commands=['weather', 'погода'])
def weather_2(message):
    weather(message)

@bot.message_handler(commands=['information'])
def infa(message):
    information(message)

@bot.message_handler(commands=['site_weather', 'website_weather', 'сайт_погода'])
def site(message):
    site_with_weather(message)

@bot.message_handler(commands=['commands'])
def com(message):
    commands(message)

# обработка текстовых сообщений пользователя c файла messagehandler
@bot.message_handler()
def massage_w(message):
    info(message)

'''
Необходимо, чтобы программа работала постоянно, иначе бот будет работать только во время компиляции кода
'''
bot.polling(none_stop=True) # программа работает без остановки


