from pyexpat.errors import messages

from handlers.messagehandler import info
from handlers.messagehandler_2 import weather
from handlers.messagehandler_2 import information
from handlers.messagehandler_2 import commands
from handlers.messagehandler_2 import print_all_users

#
# Описание папок
# Utilits единственный файл который здесь лежит это
#          logger он перемещает команды В @BotFather (бот в тг), эти команды будут встроены в бот по умолчанию
#Handlers отвечает за обработку сообщений
#           starthandler - обработка сообщений при команде старт
#           messangehandler - обработка сообщений от пользователя
#           messangehandler_2 - обработка запросов от встроенных команд бота
# Config - конфигурация
#           main - тело бота, основной файл запуска бота
#           env - файл с зашифрованными данными
#

from bot_instance import bot
from handlers.starthandler import main
from utilits.assets import stickers, emoji

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

@bot.message_handler(commands=['commands'])
def com(message):
    commands(message)

@bot.message_handler(commands=['users'])
def print_users(message):
    # функция выводит всех пользователей
    print_all_users(message)

# обработка текстовых сообщений пользователя c файла messagehandler
@bot.message_handler()
def massage_w(message):
    info(message)

'''
Необходимо, чтобы программа работала постоянно, иначе бот будет работать только во время компиляции кода
'''
if __name__ == '__main__':
    bot.polling(none_stop=True) # программа работает без остановки



