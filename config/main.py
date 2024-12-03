from handlers.user_handlers.messagehandler import info
from handlers.user_handlers.messagehandler_2 import weather
from handlers.user_handlers.messagehandler_2 import information
from handlers.user_handlers.messagehandler_2 import commands
from models.classification import clothes_response
from handlers.buttons_functions import buttons

import warnings
warnings.filterwarnings("ignore")

from bot_instance import bot
from handlers.user_handlers.starthandler import main

# обработка команды старт; команда в папке user_handlers в starthandler
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
if __name__ == '__main__':
    bot.polling(none_stop=True) # программа работает без остановки



